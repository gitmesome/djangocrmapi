from rest_framework import generics
from rest_framework.response import Response
from crm.models.product import Product  # Update with actual path
from .serializers import ProductSerializer
from django.conf import settings
import json

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(id__in=settings.PUBLIC_PRODUCTS)
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        #json_data = json.dumps(serializer.data)
        json_data = serializer.data
        return Response(json_data, content_type='application/json')


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(id__in=settings.PUBLIC_PRODUCTS)
    serializer_class = ProductSerializer
