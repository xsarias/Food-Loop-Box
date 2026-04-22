"""
Products models for Food Loop Box application
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import Compartment, BusinessPartner
from apps.authentication.models import User


class FoodCategory(models.Model):
    """Categories for food products"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Food Category"
        verbose_name_plural = "Food Categories"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Food products registered for donation or sale"""
    
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('reserved', 'Reservado'),
        ('collected', 'Recolectado'),
        ('expired', 'Vencido'),
        ('removed', 'Removido'),
    ]
    
    PRODUCT_TYPE = [
        ('donation', 'Donación'),
        ('sale', 'Venta'),
    ]
    
    # Basic information
    name = models.CharField(max_length=255)
    category = models.ForeignKey(FoodCategory, on_delete=models.PROTECT, related_name='products')
    description = models.TextField(blank=True)
    
    # Provider information
    provider = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, related_name='products')
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registered_products')
    
    # Status and type
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE)
    
    # Physical information
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    unit = models.CharField(max_length=20, choices=[
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('L', 'Litros'),
        ('ml', 'Mililitros'),
        ('unit', 'Unidad'),
    ])
    
    # Pricing (for sale products)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    discount_percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Temperature control
    required_temperature = models.FloatField(default=4.0, help_text="Temperature in Celsius")
    temperature_min = models.FloatField(default=2.0)
    temperature_max = models.FloatField(default=6.0)
    
    # Expiration and dates
    registration_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    expiration_alert_sent = models.BooleanField(default=False)
    
    # Storage location
    compartment = models.ForeignKey(Compartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # Tracking
    is_reserved = models.BooleanField(default=False)
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reserved_products')
    reservation_date = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['expiration_date']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.provider.name}"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expiration_date
    
    @property
    def final_price(self):
        """Return the final price (discounted if it's a sale)"""
        if self.product_type == 'donation':
            return 0
        return self.discounted_price or self.original_price
