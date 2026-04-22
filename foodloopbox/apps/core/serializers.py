"""
Serializers for Core app
"""

from rest_framework import serializers
from apps.core.models import Location, BusinessPartner, SmartDevice, Compartment


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model"""
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'location_type', 'address', 'city', 'postal_code',
            'latitude', 'longitude', 'phone', 'email', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BusinessPartnerSerializer(serializers.ModelSerializer):
    """Serializer for BusinessPartner model"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = BusinessPartner
        fields = [
            'id', 'name', 'partner_type', 'location', 'location_name',
            'contact_person', 'email', 'phone', 'business_id', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompartmentSerializer(serializers.ModelSerializer):
    """Serializer for Compartment model"""
    
    device_name = serializers.CharField(source='device.device_id', read_only=True)
    
    class Meta:
        model = Compartment
        fields = [
            'id', 'device', 'device_name', 'compartment_number', 'status',
            'current_temperature', 'temperature_setpoint', 'is_locked',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SmartDeviceSerializer(serializers.ModelSerializer):
    """Serializer for SmartDevice model"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    compartments = CompartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = SmartDevice
        fields = [
            'id', 'device_id', 'location', 'location_name', 'status',
            'total_compartments', 'available_compartments', 'current_temperature',
            'refrigeration_power', 'last_maintenance', 'last_sync', 'is_online',
            'compartments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'compartments']


class SmartDeviceDetailSerializer(SmartDeviceSerializer):
    """Extended serializer with compartment details"""
    pass


class LocationDetailSerializer(LocationSerializer):
    """Extended location serializer with partners and device"""
    
    partners = BusinessPartnerSerializer(many=True, read_only=True)
    device = SmartDeviceSerializer(read_only=True)
    
    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ['partners', 'device']
