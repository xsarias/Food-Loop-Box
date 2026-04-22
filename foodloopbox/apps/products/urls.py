"""
URLs for Products app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.viewsets import FoodCategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', FoodCategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
