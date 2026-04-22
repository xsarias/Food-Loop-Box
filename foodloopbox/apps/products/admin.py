"""
Admin configuration for Products app
"""

from django.contrib import admin
from apps.products.models import FoodCategory, Product


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'provider', 'status', 'product_type', 'quantity', 'unit', 'expiration_date', 'created_at')
    list_filter = ('status', 'product_type', 'category', 'provider', 'created_at', 'expiration_date')
    search_fields = ('name', 'description', 'provider__name')
    readonly_fields = ('created_at', 'updated_at', 'registration_date')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Provider', {
            'fields': ('provider', 'registered_by')
        }),
        ('Type & Status', {
            'fields': ('product_type', 'status', 'is_reserved', 'reserved_by')
        }),
        ('Quantity', {
            'fields': ('quantity', 'unit')
        }),
        ('Pricing', {
            'fields': ('original_price', 'discounted_price', 'discount_percentage')
        }),
        ('Temperature Control', {
            'fields': ('required_temperature', 'temperature_min', 'temperature_max')
        }),
        ('Dates', {
            'fields': ('registration_date', 'expiration_date', 'reservation_date', 'expiration_alert_sent')
        }),
        ('Storage', {
            'fields': ('compartment',)
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
