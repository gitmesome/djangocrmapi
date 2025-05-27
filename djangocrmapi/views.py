from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from crm.models.product import Product  # Update with actual path
from .serializers import ProductSerializer, CustomerFormSerializer
from django.conf import settings
import json
import logging
import requests

logger = logging.getLogger(__name__)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(id__in=settings.PUBLIC_PRODUCTS)
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        json_data = json.dumps(serializer.data)
        # json_data = serializer.data
        return Response(json_data, content_type='application/json')


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(id__in=settings.PUBLIC_PRODUCTS)
    serializer_class = ProductSerializer


class CustomerFormView(APIView):
    permission_classes = []  # Use IsAuthenticated if this requires login
    throttle_scope = 'form_submission'

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
            return False, "reCAPTCHA failed"
        if result.get("action") != action_expected:
            return False, "Unexpected reCAPTCHA action"
        if result.get("score", 0) < score_threshold:
            return False, "Low reCAPTCHA score"
        return True, None


    def post(self, request, format=None):
        import pdb;pdb.set_trace()
        serializer = CustomerFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Example: log or save data (replace this with model.save() if needed)
        logger.info("New customer form submitted: %s", serializer.validated_data)

        is_valid, reason = verify_recaptcha(serializer.validated_data["recaptcha_token"])
        if not is_valid:
            return Response({"detail": f"reCAPTCHA failed: {reason}"}, status=400)

        # Step 2: Process form
        validated = serializer.validated_data
        return Response({"message": "Form submitted successfully"}, status=status.HTTP_201_CREATED)

