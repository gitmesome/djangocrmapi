from rest_framework import serializers
from .models import CustomerFormSubmission
from crm.models.product import Product  # Update with actual path
import re
import bleach

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'currency',
            'product_category', 'on_sale', 'type'
        ]

class CustomerFormSerializer(serializers.ModelSerializer):
    recaptcha_token = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerFormSubmission
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'city',
            'state', 'zip', 'lat', 'lng', 'job_type', 'message', 'service_date',
            'recaptcha_token'
        ]

    # Optional: extra validation for phone and zip formats
    phone = serializers.RegexField(regex=r'^\(\d{3}\) \d{3}-\d{4}$')
    zip = serializers.RegexField(regex=r'^\d{5}(-\d{4})?$')
    service_date = serializers.DateTimeField(
        format="%Y-%m-%d",
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%Y-%m-%dT%H:%M:%S.%fZ']
    )

    def validate_message(self, value):
        return bleach.clean(value, tags=[], strip=True)

    def create(self, validated_data):
        validated_data.pop('recaptcha_token', None)
        return CustomerFormSubmission.objects.create(**validated_data)
    

