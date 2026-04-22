"""
Serializers for Analytics app
"""

from rest_framework import serializers
from apps.analytics.models import (
    DailyStatistics, LocationMetrics, PartnerMetrics,
    EnvironmentalImpact, UserActivityReport
)


class DailyStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for DailyStatistics model"""
    
    class Meta:
        model = DailyStatistics
        fields = [
            'id', 'date', 'total_products_registered', 'total_products_donated',
            'total_products_sold', 'total_products_expired', 'total_weight_rescued',
            'total_weight_donated', 'total_weight_sold', 'total_transactions',
            'total_amount', 'new_users', 'active_users', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class LocationMetricsSerializer(serializers.ModelSerializer):
    """Serializer for LocationMetrics model"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = LocationMetrics
        fields = [
            'id', 'location', 'location_name', 'total_products_handled',
            'total_weight_rescued', 'average_products_per_day', 'total_revenue',
            'average_transaction_value', 'unique_customers', 'repeat_customers',
            'estimated_co2_saved', 'estimated_water_saved', 'last_updated'
        ]
        read_only_fields = fields


class PartnerMetricsSerializer(serializers.ModelSerializer):
    """Serializer for PartnerMetrics model"""
    
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    
    class Meta:
        model = PartnerMetrics
        fields = [
            'id', 'partner', 'partner_name', 'total_products_donated',
            'total_weight_donated', 'average_donation_per_day', 'total_products_sold',
            'total_revenue_from_sales', 'lives_impacted', 'total_waste_prevented',
            'last_updated'
        ]
        read_only_fields = fields


class EnvironmentalImpactSerializer(serializers.ModelSerializer):
    """Serializer for EnvironmentalImpact model"""
    
    class Meta:
        model = EnvironmentalImpact
        fields = [
            'id', 'start_date', 'end_date', 'period_name',
            'total_food_rescued_kg', 'estimated_co2_avoided_kg',
            'estimated_water_saved_liters', 'estimated_energy_saved_kwh',
            'people_fed', 'families_supported', 'estimated_value_rescued',
            'created_at'
        ]
        read_only_fields = fields


class UserActivityReportSerializer(serializers.ModelSerializer):
    """Serializer for UserActivityReport model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserActivityReport
        fields = [
            'id', 'user', 'user_username', 'user_email', 'total_purchases',
            'total_amount_spent', 'average_purchase_value', 'total_donations_received',
            'total_weight_received', 'days_active', 'last_activity_date',
            'co2_saved_through_purchases', 'last_updated'
        ]
        read_only_fields = fields


class AnalyticsDashboardSerializer(serializers.Serializer):
    """Serializer for analytics dashboard data"""
    
    today_statistics = DailyStatisticsSerializer()
    overall_statistics = serializers.SerializerMethodField()
    top_locations = LocationMetricsSerializer(many=True)
    top_partners = PartnerMetricsSerializer(many=True)
    environmental_impact = EnvironmentalImpactSerializer()
    
    def get_overall_statistics(self, obj):
        return {
            'total_products_handled': obj.get('total_products_handled', 0),
            'total_weight_rescued': obj.get('total_weight_rescued', 0),
            'total_revenue': obj.get('total_revenue', 0),
            'total_transactions': obj.get('total_transactions', 0),
        }
