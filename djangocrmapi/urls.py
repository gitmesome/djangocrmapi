from django.urls import path
from .views import ProductListView, ProductDetailView, CustomerFormView

app_name = 'djangocrmapi'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('submit-form/', CustomerFormView.as_view(), name='customer-form'),
]
