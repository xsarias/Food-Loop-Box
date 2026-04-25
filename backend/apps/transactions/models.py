"""
Transactions models for Food Loop Box application
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.authentication.models import User
from apps.products.models import Product
from apps.core.models import SmartDevice


class Transaction(models.Model):
    """Financial transactions for purchased products"""
    
    TRANSACTION_STATUS = [
        ('pending', 'Pendiente'),
        ('completed', 'Completada'),
        ('failed', 'Fallida'),
        ('cancelled', 'Cancelada'),
    ]
    
    PAYMENT_METHOD = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('mobile_payment', 'Pago Móvil'),
        ('transfer', 'Transferencia'),
    ]
    
    # Transaction information
    transaction_id = models.CharField(max_length=100, unique=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='COP')
    
    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    
    # Withdrawal code
    withdrawal_code = models.CharField(max_length=50, unique=True)
    withdrawal_code_used = models.BooleanField(default=False)
    withdrawal_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=['buyer', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['withdrawal_code']),
        ]
    
    def __str__(self):
        return f"{self.transaction_id} - {self.buyer.username}"


class Reservation(models.Model):
    """Product reservations made by users"""
    
    RESERVATION_STATUS = [
        ('active', 'Activa'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('expired', 'Expirada'),
    ]
    
    # Reservation information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS, default='active')
    
    # Dates
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    collection_date = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reservation_date']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['product', 'status']),
            models.Index(fields=['expiration_date']),
        ]
    
    def __str__(self):
        return f"Reservation {self.id} - {self.product.name}"


class Collection(models.Model):
    """Product collection records"""
    
    COLLECTION_STATUS = [
        ('scheduled', 'Programada'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completada'),
        ('failed', 'Fallida'),
    ]
    
    # Collection information
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='collections')
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='collections')
    status = models.CharField(max_length=20, choices=COLLECTION_STATUS, default='scheduled')
    
    # Device information
    device = models.ForeignKey(SmartDevice, on_delete=models.SET_NULL, null=True, blank=True, related_name='collections')
    
    # Dates
    scheduled_date = models.DateTimeField()
    actual_collection_date = models.DateTimeField(null=True, blank=True)
    
    # Verification
    withdrawal_code = models.CharField(max_length=50, blank=True)
    code_verified = models.BooleanField(default=False)
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['product', 'status']),
        ]
    
    def __str__(self):
        return f"Collection {self.id} - {self.product.name}"


class DeviceInteraction(models.Model):
    """Interactions with Smart Devices (opening compartments, etc)"""
    
    INTERACTION_TYPE = [
        ('compartment_open', 'Apertura de Compartimiento'),
        ('code_validation', 'Validación de Código'),
        ('compartment_close', 'Cierre de Compartimiento'),
        ('error', 'Error'),
    ]
    
    # Interaction information
    device = models.ForeignKey(SmartDevice, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='device_interactions')
    interaction_type = models.CharField(max_length=30, choices=INTERACTION_TYPE)
    
    # Details
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    withdrawal_code = models.CharField(max_length=50, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Device Interaction"
        verbose_name_plural = "Device Interactions"
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.device.device_id} - {self.interaction_type}"
