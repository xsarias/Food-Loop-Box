"""
URLs for Transactions app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.transactions.viewsets import (
    TransactionViewSet, ReservationViewSet,
    CollectionViewSet, DeviceInteractionViewSet
)
from apps.transactions.viewsets import LockerViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'device-interactions', DeviceInteractionViewSet, basename='device-interaction')
router.register(r'lockers', LockerViewSet, basename='locker')

urlpatterns = [
    path('', include(router.urls)),
]
