"""
Admin configuration for Core app
"""

from django.contrib import admin
from apps.core.models import Location, BusinessPartner, SmartDevice, Compartment


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type', 'city', 'is_active', 'created_at')
    list_filter = ('location_type', 'city', 'is_active', 'created_at')
    search_fields = ('name', 'address', 'city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location_type', 'address', 'city', 'postal_code')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(BusinessPartner)
class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'location', 'is_active', 'created_at')
    list_filter = ('partner_type', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'phone', 'business_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'partner_type', 'location')
        }),
        ('Contact', {
            'fields': ('contact_person', 'email', 'phone')
        }),
        ('Business', {
            'fields': ('business_id',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SmartDevice)
class SmartDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'location', 'status', 'is_online', 'available_compartments', 'created_at')
    list_filter = ('status', 'is_online', 'created_at')
    search_fields = ('device_id', 'location__name')
    readonly_fields = ('created_at', 'updated_at', 'last_sync')
    fieldsets = (
        ('Basic Information', {
            'fields': ('device_id', 'location', 'status')
        }),
        ('Compartments', {
            'fields': ('total_compartments', 'available_compartments')
        }),
        ('Temperature', {
            'fields': ('current_temperature', 'refrigeration_power')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance', 'is_online')
        }),
        ('Metadata', {
            'fields': ('last_sync', 'created_at', 'updated_at')
        }),
    )


@admin.register(Compartment)
class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('device', 'compartment_number', 'status', 'is_locked', 'created_at')
    list_filter = ('status', 'is_locked', 'device', 'created_at')
    search_fields = ('device__device_id',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('device', 'compartment_number')
        }),
        ('Status', {
            'fields': ('status', 'is_locked')
        }),
        ('Temperature', {
            'fields': ('current_temperature', 'temperature_setpoint')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
