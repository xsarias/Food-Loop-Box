"""
URLs for Core app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.viewsets import (
    LocationViewSet, BusinessPartnerViewSet,
    SmartDeviceViewSet, CompartmentViewSet
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'partners', BusinessPartnerViewSet, basename='business-partner')
router.register(r'devices', SmartDeviceViewSet, basename='smart-device')
router.register(r'compartments', CompartmentViewSet, basename='compartment')

urlpatterns = [
    path('', include(router.urls)),
]
