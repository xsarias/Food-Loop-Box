"""
URLs for Analytics app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.analytics.viewsets import (
    DailyStatisticsViewSet, LocationMetricsViewSet,
    PartnerMetricsViewSet, EnvironmentalImpactViewSet,
    UserActivityReportViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'daily-statistics', DailyStatisticsViewSet, basename='daily-statistics')
router.register(r'location-metrics', LocationMetricsViewSet, basename='location-metrics')
router.register(r'partner-metrics', PartnerMetricsViewSet, basename='partner-metrics')
router.register(r'environmental-impact', EnvironmentalImpactViewSet, basename='environmental-impact')
router.register(r'user-activity', UserActivityReportViewSet, basename='user-activity')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
