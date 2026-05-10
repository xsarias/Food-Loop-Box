"""
Viewsets (Controllers) for Analytics app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Sum, Count, Avg, Case, When, F, FloatField, Value, ExpressionWrapper
from django.utils import timezone
from datetime import timedelta, datetime, time
from apps.analytics.models import (
    DailyStatistics, LocationMetrics, PartnerMetrics,
    EnvironmentalImpact, UserActivityReport
)
from apps.analytics.serializers import (
    DailyStatisticsSerializer, LocationMetricsSerializer,
    PartnerMetricsSerializer, EnvironmentalImpactSerializer,
    UserActivityReportSerializer
)


class DailyStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for DailyStatistics
    
    Read-only access to daily statistics
    """
    queryset = DailyStatistics.objects.all()
    serializer_class = DailyStatisticsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['date']
    ordering_fields = ['date']
    ordering = ['-date']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def today(self, request):
        """Get today's statistics"""
        today = timezone.now().date()
        stats, created = DailyStatistics.objects.get_or_create(date=today)
        
        serializer = self.get_serializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def week_summary(self, request):
        """Get last 7 days statistics"""
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        stats = DailyStatistics.objects.filter(date__range=[week_ago, today]).order_by('date')
        
        serializer = self.get_serializer(stats, many=True)
        
        # Calculate totals
        totals = stats.aggregate(
            total_products=Sum('total_products_registered'),
            total_weight=Sum('total_weight_rescued'),
            total_amount=Sum('total_amount'),
            total_transactions=Sum('total_transactions'),
        )
        
        return Response({
            'daily_stats': serializer.data,
            'totals': totals
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def month_summary(self, request):
        """Get last 30 days statistics"""
        today = timezone.now().date()
        month_ago = today - timedelta(days=30)
        
        stats = DailyStatistics.objects.filter(date__range=[month_ago, today]).order_by('date')
        
        serializer = self.get_serializer(stats, many=True)
        
        # Calculate totals
        totals = stats.aggregate(
            total_products=Sum('total_products_registered'),
            total_weight=Sum('total_weight_rescued'),
            total_amount=Sum('total_amount'),
            total_transactions=Sum('total_transactions'),
            avg_daily_transactions=Avg('total_transactions'),
        )
        
        return Response({
            'daily_stats': serializer.data,
            'totals': totals
        })


class LocationMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for LocationMetrics
    
    Read-only access to location metrics
    """
    queryset = LocationMetrics.objects.select_related('location')
    serializer_class = LocationMetricsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['location']
    ordering_fields = ['total_weight_rescued', 'total_revenue']
    ordering = ['-total_weight_rescued']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def top_locations(self, request):
        """Get top performing locations"""
        limit = int(request.query_params.get('limit', 10))
        
        metrics = LocationMetrics.objects.order_by('-total_weight_rescued')[:limit]
        serializer = self.get_serializer(metrics, many=True)
        
        return Response({
            'count': len(metrics),
            'locations': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def by_revenue(self, request):
        """Get locations sorted by revenue"""
        limit = int(request.query_params.get('limit', 10))
        
        metrics = LocationMetrics.objects.order_by('-total_revenue')[:limit]
        serializer = self.get_serializer(metrics, many=True)
        
        return Response({
            'count': len(metrics),
            'locations': serializer.data
        })


class PartnerMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for PartnerMetrics
    
    Read-only access to partner metrics
    """
    queryset = PartnerMetrics.objects.select_related('partner')
    serializer_class = PartnerMetricsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['partner']
    ordering_fields = ['total_weight_donated', 'total_revenue_from_sales']
    ordering = ['-total_weight_donated']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def top_partners(self, request):
        """Get top performing partners"""
        limit = int(request.query_params.get('limit', 10))
        
        metrics = PartnerMetrics.objects.order_by('-total_weight_donated')[:limit]
        serializer = self.get_serializer(metrics, many=True)
        
        return Response({
            'count': len(metrics),
            'partners': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def by_impact(self, request):
        """Get partners sorted by lives impacted"""
        limit = int(request.query_params.get('limit', 10))
        
        metrics = PartnerMetrics.objects.order_by('-lives_impacted')[:limit]
        serializer = self.get_serializer(metrics, many=True)
        
        return Response({
            'count': len(metrics),
            'partners': serializer.data
        })


class EnvironmentalImpactViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for EnvironmentalImpact
    
    Read-only access to environmental impact reports
    """
    queryset = EnvironmentalImpact.objects.all()
    serializer_class = EnvironmentalImpactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['end_date', 'total_food_rescued_kg']
    ordering = ['-end_date']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def latest(self, request):
        """Get latest environmental impact report"""
        impact = EnvironmentalImpact.objects.latest('end_date')
        
        serializer = self.get_serializer(impact)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def summary(self, request):
        """Get summary of all environmental impacts"""
        impacts = EnvironmentalImpact.objects.all()
        
        summary = impacts.aggregate(
            total_food_kg=Sum('total_food_rescued_kg'),
            total_co2_avoided=Sum('estimated_co2_avoided_kg'),
            total_water_saved=Sum('estimated_water_saved_liters'),
            total_people_fed=Sum('people_fed'),
            total_families_supported=Sum('families_supported'),
            total_value=Sum('estimated_value_rescued'),
        )
        
        return Response({
            'summary': summary,
            'number_of_reports': impacts.count()
        })


class UserActivityReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for UserActivityReport
    
    Read-only access to user activity reports
    """
    queryset = UserActivityReport.objects.select_related('user')
    serializer_class = UserActivityReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If not admin, only show own activity
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_activity(self, request):
        """Get current user's activity report"""
        try:
            report = UserActivityReport.objects.get(user=request.user)
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        except UserActivityReport.DoesNotExist:
            return Response(
                {'detail': 'No activity report found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def top_users(self, request):
        """Get top active users"""
        limit = int(request.query_params.get('limit', 10))
        
        reports = UserActivityReport.objects.order_by('-days_active')[:limit]
        serializer = self.get_serializer(reports, many=True)
        
        return Response({
            'count': len(reports),
            'users': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def top_spenders(self, request):
        """Get users who have spent the most"""
        limit = int(request.query_params.get('limit', 10))
        
        reports = UserActivityReport.objects.order_by('-total_amount_spent')[:limit]
        serializer = self.get_serializer(reports, many=True)
        
        return Response({
            'count': len(reports),
            'users': serializer.data
        })


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet for dashboard analytics
    
    Aggregated analytics data for dashboard
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get complete dashboard overview — computed live from product/transaction data."""
        from django.contrib.auth import get_user_model
        from apps.products.models import Product
        from apps.transactions.models import Transaction, Reservation

        User = get_user_model()

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)

        # Normalize weight to kg (kg→kg, g→kg, others→0)
        weight_expr = ExpressionWrapper(
            Case(
                When(unit='kg', then=F('quantity')),
                When(unit='g', then=F('quantity') / Value(1000.0)),
                default=Value(0.0),
                output_field=FloatField(),
            ),
            output_field=FloatField(),
        )

        # ── This week ──────────────────────────────────────────────────────────
        week_prods = Product.objects.filter(registration_date__gte=week_start)
        week_txns = Transaction.objects.filter(created_at__gte=week_start, status='completed')
        week_weight = week_prods.annotate(w=weight_expr).aggregate(s=Sum('w'))['s'] or 0

        this_week = {
            'total_products': week_prods.count(),
            'total_weight': round(week_weight, 2),
            'total_amount': float(week_txns.aggregate(s=Sum('amount'))['s'] or 0),
            'total_transactions': week_txns.count(),
        }

        # ── Today ──────────────────────────────────────────────────────────────
        today_prods = Product.objects.filter(registration_date__gte=today_start)
        today_donated = Product.objects.filter(
            product_type='donation', status='collected', updated_at__gte=today_start
        )
        today_sold = Product.objects.filter(
            product_type='sale', status='collected', updated_at__gte=today_start
        )
        today_expired = Product.objects.filter(
            expiration_date__date=now.date(), status='expired'
        )
        today_active = (
            Reservation.objects.filter(reservation_date__gte=today_start)
            .values('user').distinct().count()
        )

        today_stats = {
            'total_products_registered': today_prods.count(),
            'total_products_donated': today_donated.count(),
            'total_products_sold': today_sold.count(),
            'total_products_expired': today_expired.count(),
            'new_users': User.objects.filter(date_joined__gte=today_start).count(),
            'active_users': today_active,
        }

        # ── Top partners ───────────────────────────────────────────────────────
        partner_rows = (
            Product.objects.filter(product_type='donation')
            .values('provider__id', 'provider__name')
            .annotate(cnt=Count('id'))
            .order_by('-cnt')[:5]
        )
        top_partners = []
        for row in partner_rows:
            pid = row['provider__id']
            weight = float(
                Product.objects.filter(provider_id=pid, product_type='donation')
                .annotate(w=weight_expr).aggregate(s=Sum('w'))['s'] or 0
            )
            revenue = float(
                Transaction.objects.filter(
                    product__provider_id=pid, product__product_type='sale', status='completed'
                ).aggregate(s=Sum('amount'))['s'] or 0
            )
            lives = Product.objects.filter(
                provider_id=pid, product_type='donation', status='collected'
            ).count()
            top_partners.append({
                'id': pid,
                'partner_name': row['provider__name'],
                'total_weight_donated': round(weight, 2),
                'lives_impacted': lives,
                'total_revenue_from_sales': revenue,
            })

        # ── Top locations ──────────────────────────────────────────────────────
        location_rows = (
            Product.objects.filter(provider__location__isnull=False)
            .values('provider__location__id', 'provider__location__name')
            .annotate(cnt=Count('id'))
            .order_by('-cnt')[:5]
        )
        top_locations = []
        for row in location_rows:
            lid = row['provider__location__id']
            weight = float(
                Product.objects.filter(provider__location_id=lid)
                .annotate(w=weight_expr).aggregate(s=Sum('w'))['s'] or 0
            )
            revenue = float(
                Transaction.objects.filter(
                    product__provider__location_id=lid, status='completed'
                ).aggregate(s=Sum('amount'))['s'] or 0
            )
            unique_customers = (
                Transaction.objects.filter(
                    product__provider__location_id=lid, status='completed'
                ).values('buyer').distinct().count()
            )
            top_locations.append({
                'id': lid,
                'location_name': row['provider__location__name'],
                'total_weight_rescued': round(weight, 2),
                'unique_customers': unique_customers,
                'total_revenue': revenue,
            })

        # ── Environmental impact ───────────────────────────────────────────────
        try:
            latest_impact = EnvironmentalImpact.objects.latest('end_date')
            impact_data = EnvironmentalImpactSerializer(latest_impact).data
        except EnvironmentalImpact.DoesNotExist:
            total_kg = float(
                Product.objects.filter(status='collected')
                .annotate(w=weight_expr).aggregate(s=Sum('w'))['s'] or 0
            )
            if total_kg > 0:
                impact_data = {
                    'estimated_co2_avoided_kg': round(total_kg * 2.5, 2),
                    'estimated_water_saved_liters': round(total_kg * 1000, 0),
                    'people_fed': int(total_kg / 0.5),
                    'families_supported': int(total_kg / 3.0),
                }
            else:
                impact_data = None

        return Response({
            'today': today_stats,
            'this_week': this_week,
            'top_locations': top_locations,
            'top_partners': top_partners,
            'environmental_impact': impact_data,
        })
