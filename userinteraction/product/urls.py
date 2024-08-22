from django.urls import path
from .views import ProductDetailView, ProductListView


urlpatterns = [
    path('product/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product', ProductListView.as_view(), name='product-list'),
]
