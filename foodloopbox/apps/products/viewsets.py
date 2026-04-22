"""
Viewsets (Controllers) for Products app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
from apps.products.models import FoodCategory, Product
from apps.products.serializers import (
    FoodCategorySerializer, ProductSerializer, ProductListSerializer,
    ProductCreateSerializer, ProductUpdateSerializer, ProductDetailSerializer
)


class FoodCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FoodCategory management
    
    Provides CRUD operations for food categories
    """
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product management
    
    Provides CRUD operations for food products
    """
    queryset = Product.objects.select_related('category', 'provider', 'registered_by', 'reserved_by')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'product_type', 'category', 'provider', 'is_reserved']
    search_fields = ['name', 'description', 'provider__name']
    ordering_fields = ['name', 'expiration_date', 'created_at', 'final_price']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by expiration (available products not expired)
        only_available = self.request.query_params.get('only_available')
        if only_available == 'true':
            queryset = queryset.filter(
                status='available',
                expiration_date__gt=timezone.now()
            )
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create']:
            # Only partners/admins can create products
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Create a new product and assign it to registered_by"""
        serializer.save(registered_by=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def available(self, request):
        """Get all available products not yet expired"""
        products = self.get_queryset().filter(
            status='available',
            expiration_date__gt=timezone.now()
        )
        
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'count': products.count(),
            'products': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def expiring_soon(self, request):
        """Get products expiring within 24 hours"""
        now = timezone.now()
        soon = now + timedelta(hours=24)
        
        products = self.get_queryset().filter(
            status='available',
            expiration_date__gt=now,
            expiration_date__lte=soon
        )
        
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'count': products.count(),
            'products': serializer.data,
            'message': 'Productos próximos a vencer'
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def expired(self, request):
        """Get expired products"""
        products = self.get_queryset().filter(
            expiration_date__lt=timezone.now()
        )
        
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'count': products.count(),
            'products': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reserve(self, request, pk=None):
        """Reserve a product"""
        product = self.get_object()
        
        if product.is_reserved:
            return Response(
                {'detail': 'Producto ya está reservado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if product.status != 'available':
            return Response(
                {'detail': 'Producto no está disponible'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.is_reserved = True
        product.reserved_by = request.user
        product.reservation_date = timezone.now()
        product.save()
        
        # Create reservation record
        from apps.transactions.models import Reservation
        expiration_date = timezone.now() + timedelta(days=3)
        Reservation.objects.create(
            user=request.user,
            product=product,
            expiration_date=expiration_date,
            status='active'
        )
        
        serializer = self.get_serializer(product)
        return Response({
            'detail': 'Producto reservado exitosamente',
            'product': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_reservation(self, request, pk=None):
        """Cancel product reservation"""
        product = self.get_object()
        
        if not product.is_reserved:
            return Response(
                {'detail': 'Producto no está reservado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if product.reserved_by != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permiso para cancelar esta reserva'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        product.is_reserved = False
        product.reserved_by = None
        product.reservation_date = None
        product.save()
        
        # Cancel reservation record
        from apps.transactions.models import Reservation
        Reservation.objects.filter(
            product=product,
            user=request.user,
            status='active'
        ).update(status='cancelled')
        
        serializer = self.get_serializer(product)
        return Response({
            'detail': 'Reserva cancelada exitosamente',
            'product': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def mark_expired(self, request, pk=None):
        """Mark a product as expired"""
        product = self.get_object()
        product.status = 'expired'
        product.save()
        
        serializer = self.get_serializer(product)
        return Response({
            'detail': 'Producto marcado como vencido',
            'product': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def mark_collected(self, request, pk=None):
        """Mark a product as collected"""
        product = self.get_object()
        product.status = 'collected'
        product.save()
        
        serializer = self.get_serializer(product)
        return Response({
            'detail': 'Producto marcado como recolectado',
            'product': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def history(self, request, pk=None):
        """Get transaction history for a product"""
        product = self.get_object()
        
        transactions = product.transactions.all()
        from apps.transactions.serializers import TransactionListSerializer
        transactions_serializer = TransactionListSerializer(transactions, many=True)
        
        reservations = product.reservations.all()
        from apps.transactions.serializers import ReservationListSerializer
        reservations_serializer = ReservationListSerializer(reservations, many=True)
        
        return Response({
            'product': self.get_serializer(product).data,
            'transactions': transactions_serializer.data,
            'reservations': reservations_serializer.data
        })
