"""
Viewsets (Controllers) for Core app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.core.models import Location, BusinessPartner, SmartDevice, Compartment
from apps.core.serializers import (
    LocationSerializer, LocationDetailSerializer,
    BusinessPartnerSerializer, SmartDeviceSerializer,
    SmartDeviceDetailSerializer, CompartmentSerializer
)


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Location management
    
    Provides CRUD operations for managing Food Loop Box locations
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location_type', 'city', 'is_active']
    search_fields = ['name', 'address', 'city']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LocationDetailSerializer
        return LocationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def statistics(self, request, pk=None):
        """Get statistics for a specific location"""
        location = self.get_object()
        device = location.device if hasattr(location, 'device') else None
        
        stats = {
            'location_id': location.id,
            'location_name': location.name,
            'total_products': location.partners.count() if hasattr(location, 'partners') else 0,
            'device_status': device.status if device else 'N/A',
            'device_online': device.is_online if device else False,
        }
        return Response(stats)


class BusinessPartnerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessPartner management
    
    Provides CRUD operations for business partners
    """
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['partner_type', 'location', 'is_active']
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def products(self, request, pk=None):
        """Get all products from a specific partner"""
        partner = self.get_object()
        products = partner.products.all()
        
        from apps.products.serializers import ProductListSerializer
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class SmartDeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SmartDevice management
    
    Provides CRUD operations for smart devices
    """
    queryset = SmartDevice.objects.all()
    serializer_class = SmartDeviceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'location', 'is_online']
    search_fields = ['device_id', 'location__name']
    ordering_fields = ['device_id', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SmartDeviceDetailSerializer
        return SmartDeviceSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'toggle_maintenance']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def toggle_maintenance(self, request, pk=None):
        """Toggle device maintenance status"""
        device = self.get_object()
        if device.status == 'maintenance':
            device.status = 'active'
            message = "Device returned to active status"
        else:
            device.status = 'maintenance'
            message = "Device set to maintenance mode"
        device.save()
        return Response({'status': device.status, 'message': message})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def sync_status(self, request, pk=None):
        """Update device sync status"""
        from django.utils import timezone
        device = self.get_object()
        device.last_sync = timezone.now()
        device.is_online = True
        device.save()
        
        serializer = self.get_serializer(device)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def compartments_status(self, request, pk=None):
        """Get detailed status of all compartments"""
        device = self.get_object()
        compartments = device.compartments.all()
        serializer = CompartmentSerializer(compartments, many=True)
        return Response({
            'device_id': device.device_id,
            'total_compartments': device.total_compartments,
            'available': device.available_compartments,
            'compartments': serializer.data
        })


class CompartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Compartment management
    
    Provides CRUD operations for compartments
    """
    queryset = Compartment.objects.all()
    serializer_class = CompartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['device', 'status']
    ordering_fields = ['compartment_number', 'created_at']
    ordering = ['device', 'compartment_number']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'lock', 'unlock']:
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def lock(self, request, pk=None):
        """Lock a compartment"""
        compartment = self.get_object()
        compartment.is_locked = True
        compartment.status = 'maintenance'
        compartment.save()
        
        serializer = self.get_serializer(compartment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def unlock(self, request, pk=None):
        """Unlock a compartment"""
        compartment = self.get_object()
        compartment.is_locked = False
        compartment.status = 'available'
        compartment.save()
        
        serializer = self.get_serializer(compartment)
        return Response(serializer.data)
