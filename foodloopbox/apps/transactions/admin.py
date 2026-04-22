"""
Admin configuration for Transactions app
"""

from django.contrib import admin
from apps.transactions.models import Transaction, Reservation, Collection, DeviceInteraction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'buyer', 'product', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'buyer__username', 'product__name', 'withdrawal_code')
    readonly_fields = ('created_at', 'updated_at', 'transaction_id', 'withdrawal_code')
    fieldsets = (
        ('Transaction', {
            'fields': ('transaction_id', 'buyer', 'product')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Payment', {
            'fields': ('payment_method', 'status')
        }),
        ('Withdrawal', {
            'fields': ('withdrawal_code', 'withdrawal_code_used', 'withdrawal_date')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'status', 'reservation_date', 'expiration_date')
    list_filter = ('status', 'reservation_date', 'expiration_date')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at', 'updated_at', 'reservation_date')
    fieldsets = (
        ('Reservation', {
            'fields': ('user', 'product', 'status')
        }),
        ('Dates', {
            'fields': ('reservation_date', 'expiration_date', 'collection_date')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'status', 'device', 'collected_by', 'scheduled_date', 'actual_collection_date')
    list_filter = ('status', 'scheduled_date', 'code_verified')
    search_fields = ('product__name', 'withdrawal_code', 'collected_by__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Collection', {
            'fields': ('product', 'collected_by', 'status')
        }),
        ('Device', {
            'fields': ('device',)
        }),
        ('Dates', {
            'fields': ('scheduled_date', 'actual_collection_date')
        }),
        ('Verification', {
            'fields': ('withdrawal_code', 'code_verified')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DeviceInteraction)
class DeviceInteractionAdmin(admin.ModelAdmin):
    list_display = ('device', 'user', 'interaction_type', 'success', 'timestamp')
    list_filter = ('interaction_type', 'success', 'timestamp')
    search_fields = ('device__device_id', 'user__username', 'withdrawal_code')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('Interaction', {
            'fields': ('device', 'user', 'interaction_type')
        }),
        ('Result', {
            'fields': ('success', 'error_message')
        }),
        ('Details', {
            'fields': ('withdrawal_code',)
        }),
        ('Metadata', {
            'fields': ('timestamp',)
        }),
    )
