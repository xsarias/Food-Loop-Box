"""
Core models for Food Loop Box application
"""

from django.db import models
from django.core.validators import MinValueValidator


class Location(models.Model):
    """Locations where Food Loop Box devices are placed"""
    
    LOCATION_TYPES = [
        ('commercial_center', 'Centro Comercial'),
        ('restaurant', 'Restaurante'),
        ('supermarket', 'Supermercado'),
        ('cafe', 'Café'),
        ('other', 'Otro'),
    ]
    
    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Location"
        verbose_name_plural = "Locations"
    
    def __str__(self):
        return f"{self.name} - {self.city}"


class BusinessPartner(models.Model):
    """Business partners that provide food surpluses"""
    
    PARTNER_TYPES = [
        ('restaurant', 'Restaurante'),
        ('supermarket', 'Supermercado'),
        ('cafe', 'Café'),
        ('bakery', 'Panadería'),
        ('market', 'Mercado'),
        ('other', 'Otro'),
    ]
    
    name = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='partners')
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    business_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Business Partner"
        verbose_name_plural = "Business Partners"
    
    def __str__(self):
        return self.name


class SmartDevice(models.Model):
    """Smart devices (Food Loop Box machines) installed in locations"""
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('maintenance', 'Mantenimiento'),
        ('inactive', 'Inactivo'),
    ]
    
    device_id = models.CharField(max_length=100, unique=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='device')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_compartments = models.IntegerField(validators=[MinValueValidator(1)])
    available_compartments = models.IntegerField(validators=[MinValueValidator(0)])
    current_temperature = models.FloatField(null=True, blank=True)
    refrigeration_power = models.FloatField(default=1.0, validators=[MinValueValidator(0.0)])
    last_maintenance = models.DateTimeField(null=True, blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Smart Device"
        verbose_name_plural = "Smart Devices"
    
    def __str__(self):
        return f"Device {self.device_id} - {self.location.name}"


class Compartment(models.Model):
    """Individual compartments within a Smart Device"""
    
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('occupied', 'Ocupado'),
        ('maintenance', 'Mantenimiento'),
        ('error', 'Error'),
    ]
    
    device = models.ForeignKey(SmartDevice, on_delete=models.CASCADE, related_name='compartments')
    compartment_number = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_temperature = models.FloatField(null=True, blank=True)
    temperature_setpoint = models.FloatField(default=4.0)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['device', 'compartment_number']
        unique_together = ['device', 'compartment_number']
        verbose_name = "Compartment"
        verbose_name_plural = "Compartments"
    
    def __str__(self):
        return f"Compartment {self.compartment_number} - Device {self.device.device_id}"
