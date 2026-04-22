"""
Viewsets (Controllers) for Transactions app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from apps.transactions.models import Transaction, Reservation, Collection, DeviceInteraction
from apps.transactions.serializers import (
    TransactionSerializer, TransactionListSerializer, TransactionCreateSerializer,
    ReservationSerializer, ReservationListSerializer, ReservationCreateSerializer,
    CollectionSerializer, CollectionListSerializer,
    DeviceInteractionSerializer, DeviceInteractionLogSerializer
)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transaction management
    
    Handles purchase transactions
    """
    queryset = Transaction.objects.select_related('buyer', 'product')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'buyer']
    search_fields = ['transaction_id', 'product__name', 'buyer__username']
    ordering_fields = ['amount', 'created_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        elif self.action == 'list':
            return TransactionListSerializer
        return TransactionSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Create transaction and assign buyer"""
        serializer.save(buyer=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If not admin, only show user's own transactions
        if not self.request.user.is_staff:
            queryset = queryset.filter(buyer=self.request.user)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_transactions(self, request):
        """Get current user's transactions"""
        transactions = self.queryset.filter(buyer=request.user)
        
        serializer = TransactionListSerializer(transactions, many=True)
        return Response({
            'count': transactions.count(),
            'transactions': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def mark_completed(self, request, pk=None):
        """Mark transaction as completed"""
        transaction = self.get_object()
        
        if transaction.status == 'completed':
            return Response(
                {'detail': 'Transacción ya está completada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = 'completed'
        transaction.save()
        
        # Mark product as collected
        transaction.product.status = 'collected'
        transaction.product.save()
        
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def mark_failed(self, request, pk=None):
        """Mark transaction as failed"""
        transaction = self.get_object()
        transaction.status = 'failed'
        transaction.save()
        
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def validate_withdrawal_code(self, request, pk=None):
        """Validate withdrawal code for a transaction"""
        transaction = self.get_object()
        withdrawal_code = request.query_params.get('code')
        
        if not withdrawal_code:
            return Response(
                {'valid': False, 'message': 'Código no proporcionado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if transaction.withdrawal_code != withdrawal_code:
            return Response({
                'valid': False,
                'message': 'Código de retiro inválido'
            })
        
        if transaction.withdrawal_code_used:
            return Response({
                'valid': False,
                'message': 'Código ya ha sido utilizado'
            })
        
        return Response({
            'valid': True,
            'message': 'Código válido',
            'product': transaction.product.name,
            'compartment': transaction.product.compartment.compartment_number if transaction.product.compartment else None
        })


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reservation management
    
    Handles product reservations
    """
    queryset = Reservation.objects.select_related('user', 'product')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'user']
    search_fields = ['product__name', 'user__username']
    ordering_fields = ['reservation_date', 'expiration_date', 'status']
    ordering = ['-reservation_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'list':
            return ReservationListSerializer
        return ReservationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy', 'cancel']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Create reservation"""
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If not admin, only show user's own reservations
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_reservations(self, request):
        """Get current user's reservations"""
        reservations = self.queryset.filter(
            user=request.user,
            status__in=['active', 'completed']
        )
        
        serializer = ReservationListSerializer(reservations, many=True)
        return Response({
            'count': reservations.count(),
            'reservations': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel a reservation"""
        reservation = self.get_object()
        
        if reservation.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permiso para cancelar esta reserva'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if reservation.status not in ['active', 'completed']:
            return Response(
                {'detail': 'No se puede cancelar esta reserva'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'cancelled'
        reservation.save()
        
        # Release product reservation
        reservation.product.is_reserved = False
        reservation.product.reserved_by = None
        reservation.product.save()
        
        serializer = self.get_serializer(reservation)
        return Response({
            'detail': 'Reserva cancelada',
            'reservation': serializer.data
        })


class CollectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Collection management
    
    Handles product collections
    """
    queryset = Collection.objects.select_related('product', 'collected_by', 'device')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'device', 'collected_by']
    search_fields = ['product__name', 'withdrawal_code']
    ordering_fields = ['scheduled_date', 'actual_collection_date', 'status']
    ordering = ['-scheduled_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CollectionListSerializer
        return CollectionSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def verify_code(self, request, pk=None):
        """Verify and mark collection as completed"""
        collection = self.get_object()
        withdrawal_code = request.data.get('code')
        
        if not withdrawal_code:
            return Response(
                {'detail': 'Código no proporcionado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if collection.withdrawal_code != withdrawal_code:
            return Response(
                {'detail': 'Código inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        collection.code_verified = True
        collection.status = 'completed'
        collection.actual_collection_date = timezone.now()
        collection.collected_by = request.user
        collection.save()
        
        # Update product status
        collection.product.status = 'collected'
        collection.product.save()
        
        serializer = self.get_serializer(collection)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def mark_failed(self, request, pk=None):
        """Mark collection as failed"""
        collection = self.get_object()
        collection.status = 'failed'
        collection.save()
        
        serializer = self.get_serializer(collection)
        return Response(serializer.data)


class DeviceInteractionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for DeviceInteraction logging
    
    Read-only access to device interactions
    """
    queryset = DeviceInteraction.objects.select_related('device', 'user')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['device', 'interaction_type', 'success']
    search_fields = ['device__device_id', 'withdrawal_code']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeviceInteractionLogSerializer
        return DeviceInteractionSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def log_interaction(self, request):
        """Log a device interaction"""
        serializer = DeviceInteractionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
