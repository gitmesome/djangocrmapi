from rest_framework import serializers
from crm.models.product import Product  # Update with actual path
import re

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'currency',
            'product_category', 'on_sale', 'type'
        ]

class CustomerFormSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.RegexField(regex=r'^\(\d{3}\) \d{3}-\d{4}$')
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip = serializers.RegexField(regex=r'^\d{5}(-\d{4})?$')
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    job_type = serializers.CharField()
    message = serializers.CharField(allow_blank=True, required=False)
    service_date = serializers.DateField()

