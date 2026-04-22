"""
Analytics models for Food Loop Box application
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import Location, BusinessPartner
from apps.authentication.models import User


class DailyStatistics(models.Model):
    """Daily statistics about products and transactions"""
    
    # Date
    date = models.DateField(unique=True, db_index=True)
    
    # Product statistics
    total_products_registered = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_products_donated = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_products_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_products_expired = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Weight statistics (in kg)
    total_weight_rescued = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_weight_donated = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_weight_sold = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Transaction statistics
    total_transactions = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # User statistics
    new_users = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    active_users = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Daily Statistics"
        verbose_name_plural = "Daily Statistics"
    
    def __str__(self):
        return f"Statistics for {self.date}"


class LocationMetrics(models.Model):
    """Metrics for each location"""
    
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='metrics')
    
    # Product metrics
    total_products_handled = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_weight_rescued = models.FloatField(default=0, validators=[MinValueValidator(0)])
    average_products_per_day = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Financial metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    average_transaction_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # User engagement
    unique_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    repeat_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Environmental impact
    estimated_co2_saved = models.FloatField(default=0, validators=[MinValueValidator(0)], help_text="in kg")
    estimated_water_saved = models.FloatField(default=0, validators=[MinValueValidator(0)], help_text="in liters")
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Location Metrics"
        verbose_name_plural = "Location Metrics"
    
    def __str__(self):
        return f"Metrics for {self.location.name}"


class PartnerMetrics(models.Model):
    """Metrics for each business partner"""
    
    partner = models.OneToOneField(BusinessPartner, on_delete=models.CASCADE, related_name='metrics')
    
    # Product donation
    total_products_donated = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_weight_donated = models.FloatField(default=0, validators=[MinValueValidator(0)])
    average_donation_per_day = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Products sold
    total_products_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_revenue_from_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Impact
    lives_impacted = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_waste_prevented = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Partner Metrics"
        verbose_name_plural = "Partner Metrics"
    
    def __str__(self):
        return f"Metrics for {self.partner.name}"


class EnvironmentalImpact(models.Model):
    """Environmental impact calculations and projections"""
    
    # Time period
    start_date = models.DateField()
    end_date = models.DateField()
    period_name = models.CharField(max_length=100)
    
    # Impact metrics
    total_food_rescued_kg = models.FloatField(validators=[MinValueValidator(0)])
    estimated_co2_avoided_kg = models.FloatField(validators=[MinValueValidator(0)])
    estimated_water_saved_liters = models.FloatField(validators=[MinValueValidator(0)])
    estimated_energy_saved_kwh = models.FloatField(validators=[MinValueValidator(0)])
    
    # People impact
    people_fed = models.IntegerField(validators=[MinValueValidator(0)])
    families_supported = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Financial savings
    estimated_value_rescued = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-end_date']
        verbose_name = "Environmental Impact"
        verbose_name_plural = "Environmental Impacts"
    
    def __str__(self):
        return f"Impact Report {self.period_name}"


class UserActivityReport(models.Model):
    """User activity and engagement metrics"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='activity_report')
    
    # Purchase metrics
    total_purchases = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_purchase_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Donation metrics
    total_donations_received = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_weight_received = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Engagement
    days_active = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    last_activity_date = models.DateTimeField(null=True, blank=True)
    
    # Environmental contribution
    co2_saved_through_purchases = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Activity Report"
        verbose_name_plural = "User Activity Reports"
    
    def __str__(self):
        return f"Activity Report for {self.user.username}"
