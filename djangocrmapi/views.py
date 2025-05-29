from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from crm.models.product import Product  # Update with actual path
from .serializers import ProductSerializer, CustomerFormSerializer
from django.conf import settings
import json
import logging
import requests
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/.recaptcha.json"

logger = logging.getLogger(__name__)


class ProductListView(generics.ListAPIView):
    if not settings.PUBLIC_PRODUCTS:
        raise AssertionError('Please set a value for PUBLIC_PRODUCTS in the settings.py file')
    queryset = Product.objects.filter(id__in=settings.PUBLIC_PRODUCTS)
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # json_data = json.dumps(serializer.data)
        json_data = serializer.data
        return Response(json_data, content_type='application/json')


class ProductDetailView(generics.RetrieveAPIView):
    if not settings.PUBLIC_PRODUCTS:
        raise AssertionError('Please set a value for PUBLIC_PRODUCTS in the settings.py file')
    queryset = Product.objects.filter(id__in=settings.PUBLIC_PRODUCTS)
    serializer_class = ProductSerializer


class CustomerFormView(APIView):
    permission_classes = []  # Use IsAuthenticated if this requires login
    throttle_scope = 'form_submission'


    def post(self, request, format=None):
        # For now, this method is not being used due to key errors, but we 
        # may want it later as it is a copy and paste from google.
        def create_assessment(
            project_id: str, recaptcha_key: str, token: str, recaptcha_action: str
        ) -> Assessment:
            """Create an assessment to analyze the risk of a UI action.
            Args:
                project_id: Your Google Cloud Project ID.
                recaptcha_key: The reCAPTCHA key associated with the site/app
                token: The generated token obtained from the client.
                recaptcha_action: Action name corresponding to the token.
            """

            client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

            # Set the properties of the event to be tracked.
            event = recaptchaenterprise_v1.Event()
            event.site_key = recaptcha_key
            event.token = token

            assessment = recaptchaenterprise_v1.Assessment()
            assessment.event = event

            project_name = f"projects/{project_id}"

            # Build the assessment request.
            request = recaptchaenterprise_v1.CreateAssessmentRequest()
            request.assessment = assessment
            request.parent = project_name

            response = client.create_assessment(request)

            # Check if the token is valid.
            if not response.token_properties.valid:
                print(
                    "The CreateAssessment call failed because the token was "
                    + "invalid for the following reasons: "
                    + str(response.token_properties.invalid_reason)
                )
                return

            # Check if the expected action was executed.
            if response.token_properties.action != recaptcha_action:
                print(
                    "The action attribute in your reCAPTCHA tag does"
                    + "not match the action you are expecting to score"
                )
                return
            else:
                # Get the risk score and the reason(s).
                # For more information on interpreting the assessment, see:
                # https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
                for reason in response.risk_analysis.reasons:
                    print(reason)
                print(
                    "The reCAPTCHA score for this token is: "
                    + str(response.risk_analysis.score)
                )
                # Get the assessment name (id). Use this to annotate the assessment.
                assessment_name = client.parse_assessment_path(response.name).get("assessment")
                print(f"Assessment name: {assessment_name}")
            return response

        def verify_recaptcha(token, action_expected="submit_form", score_threshold=0.5):
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    "response": token
                }
            )
            result = r.json()
            if not result.get("success"):
                return False, f"reCAPTCHA failed: {result} {token}"
            if result.get("action") != action_expected:
                return False, "Unexpected reCAPTCHA action"
            if result.get("score", 0) < score_threshold:
                return False, "Low reCAPTCHA score"
            return True, None

        # import pdb;pdb.set_trace()
        serializer = CustomerFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Example: log or save data (replace this with model.save() if needed)
        all_but_recaptcha = {key:value for key, value in serializer.validated_data.items() if key != 'recaptcha_token'}
        logger.debug("New customer form submitted: %s", all_but_recaptcha)
        print(f"New customer form submitted: {all_but_recaptcha}")

        is_valid, reason = verify_recaptcha(serializer.validated_data["recaptcha_token"])
        if not is_valid:
            return Response({"detail": f"reCAPTCHA failed: {reason}"}, status=400)

        # the key is not connecting properly, but scores are being returned from
        # the verification method.  Will resolve later.
        # assessment = create_assessment(
        #    'junkinator-request-form', #settings.GOOGLE_RECAPTCHA_PROJECT_ID, 
        #    settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #    serializer.validated_data["recaptcha_token"], 'submit_form'
        #)

        instance = serializer.save()
        try:
            instance = serializer.save()
        except (IntegrityError, Exception) as e:
            logger.exception("Failed to save CustomerFormSubmission: %s", e)
            print(f"Failed to save CustomerFormSubmission: {e}")
            return Response({"detail": f"submission failed: {e}"}, status=status.HTTP_424_FAILED_DEPENDENCY)

        # Success response
        return Response(
            # hold for debugging but we not need to tell the world private info
            # {"message": "Form submitted successfully", "id": instance.id},
             {"message": "Form submitted successfully"},
            status=status.HTTP_201_CREATED
        )

        return Response({"redirect": "/thank-you"}, status=status.HTTP_302_FOUND)

