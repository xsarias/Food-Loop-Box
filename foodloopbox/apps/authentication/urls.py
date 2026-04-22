"""
URLs for Authentication app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.authentication.viewsets import (
    UserViewSet, UserPermissionViewSet, AccessLogViewSet,
    CustomTokenObtainPairView, login_view, logout_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'permissions', UserPermissionViewSet, basename='permission')
router.register(r'access-logs', AccessLogViewSet, basename='access-log')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
