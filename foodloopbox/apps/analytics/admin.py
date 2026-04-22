"""
Admin configuration for Analytics app
"""

from django.contrib import admin
from apps.analytics.models import (
    DailyStatistics, LocationMetrics, PartnerMetrics,
    EnvironmentalImpact, UserActivityReport
)


@admin.register(DailyStatistics)
class DailyStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_products_registered', 'total_weight_rescued', 'total_amount', 'updated_at')
    list_filter = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Products', {
            'fields': ('total_products_registered', 'total_products_donated', 'total_products_sold', 'total_products_expired')
        }),
        ('Weight', {
            'fields': ('total_weight_rescued', 'total_weight_donated', 'total_weight_sold')
        }),
        ('Transactions', {
            'fields': ('total_transactions', 'total_amount')
        }),
        ('Users', {
            'fields': ('new_users', 'active_users')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(LocationMetrics)
class LocationMetricsAdmin(admin.ModelAdmin):
    list_display = ('location', 'total_products_handled', 'total_weight_rescued', 'total_revenue', 'last_updated')
    list_filter = ('last_updated',)
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('Location', {
            'fields': ('location',)
        }),
        ('Products', {
            'fields': ('total_products_handled', 'total_weight_rescued', 'average_products_per_day')
        }),
        ('Financial', {
            'fields': ('total_revenue', 'average_transaction_value')
        }),
        ('Users', {
            'fields': ('unique_customers', 'repeat_customers')
        }),
        ('Environmental', {
            'fields': ('estimated_co2_saved', 'estimated_water_saved')
        }),
        ('Metadata', {
            'fields': ('last_updated',)
        }),
    )


@admin.register(PartnerMetrics)
class PartnerMetricsAdmin(admin.ModelAdmin):
    list_display = ('partner', 'total_products_donated', 'total_weight_donated', 'lives_impacted', 'last_updated')
    list_filter = ('last_updated',)
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('Partner', {
            'fields': ('partner',)
        }),
        ('Donations', {
            'fields': ('total_products_donated', 'total_weight_donated', 'average_donation_per_day')
        }),
        ('Sales', {
            'fields': ('total_products_sold', 'total_revenue_from_sales')
        }),
        ('Impact', {
            'fields': ('lives_impacted', 'total_waste_prevented')
        }),
        ('Metadata', {
            'fields': ('last_updated',)
        }),
    )


@admin.register(EnvironmentalImpact)
class EnvironmentalImpactAdmin(admin.ModelAdmin):
    list_display = ('period_name', 'start_date', 'end_date', 'total_food_rescued_kg', 'people_fed')
    list_filter = ('start_date', 'end_date')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Period', {
            'fields': ('period_name', 'start_date', 'end_date')
        }),
        ('Food Impact', {
            'fields': ('total_food_rescued_kg', 'estimated_value_rescued')
        }),
        ('Environmental Impact', {
            'fields': ('estimated_co2_avoided_kg', 'estimated_water_saved_liters', 'estimated_energy_saved_kwh')
        }),
        ('People Impact', {
            'fields': ('people_fed', 'families_supported')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(UserActivityReport)
class UserActivityReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_purchases', 'total_amount_spent', 'days_active', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Purchases', {
            'fields': ('total_purchases', 'total_amount_spent', 'average_purchase_value')
        }),
        ('Donations', {
            'fields': ('total_donations_received', 'total_weight_received')
        }),
        ('Engagement', {
            'fields': ('days_active', 'last_activity_date')
        }),
        ('Environmental', {
            'fields': ('co2_saved_through_purchases',)
        }),
        ('Metadata', {
            'fields': ('last_updated',)
        }),
    )
