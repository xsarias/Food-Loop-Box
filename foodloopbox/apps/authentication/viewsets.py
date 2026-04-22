"""
Viewsets (Controllers) for Authentication app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.authentication.models import AccessLog, UserPermission
from apps.authentication.serializers import (
    UserSerializer, UserDetailSerializer, UserRegistrationSerializer,
    UserUpdateSerializer, UserPermissionSerializer, AccessLogSerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view with additional user data"""
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management
    
    Provides CRUD operations for users and authentication
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['role', 'is_verified', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        elif self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Contraseña incorrecta'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'detail': 'Contraseña actualizada exitosamente'},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def verify(self, request, pk=None):
        """Mark user as verified"""
        user = self.get_object()
        user.is_verified = True
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def toggle_active(self, request, pk=None):
        """Toggle user active status"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        
        # Generate tokens
        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'detail': 'Usuario creado exitosamente'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserPermission management
    
    Provides CRUD operations for custom user permissions
    """
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['user', 'category']
    search_fields = ['permission_name', 'user__username']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_permissions(self, request):
        """Get current user's permissions"""
        permissions = UserPermission.objects.filter(user=request.user)
        serializer = self.get_serializer(permissions, many=True)
        return Response(serializer.data)


class AccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for AccessLog viewing
    
    Provides read-only access to login and access audit logs
    """
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['status', 'user']
    search_fields = ['email', 'ip_address']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def recent_suspicious_activity(self, request):
        """Get recent suspicious login attempts"""
        from datetime import timedelta
        from django.utils import timezone
        
        recent = timezone.now() - timedelta(hours=24)
        suspicious = AccessLog.objects.filter(
            timestamp__gte=recent,
            status__in=['failure', 'blocked']
        ).order_by('-timestamp')[:20]
        
        serializer = self.get_serializer(suspicious, many=True)
        return Response({
            'count': len(suspicious),
            'logs': serializer.data
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Custom login endpoint that logs access attempts
    """
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'detail': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    ip_address = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    if user is not None:
        # Log successful login
        AccessLog.objects.create(
            user=user,
            email=user.email,
            status='success',
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'detail': 'Login exitoso',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    else:
        # Log failed login
        AccessLog.objects.create(
            email=username,
            status='failure',
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason='Invalid credentials'
        )
        
        return Response(
            {'detail': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """
    Logout endpoint (token-based logout)
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response(
            {'detail': 'Logout exitoso'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
