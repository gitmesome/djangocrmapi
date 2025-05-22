from rest_framework import serializers
from crm.models.product import Product  # Update with actual path

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'currency',
            'product_category', 'on_sale', 'type'
        ]
