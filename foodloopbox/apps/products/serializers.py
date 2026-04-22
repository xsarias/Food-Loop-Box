"""
Serializers for Products app
"""

from rest_framework import serializers
from apps.products.models import FoodCategory, Product


class FoodCategorySerializer(serializers.ModelSerializer):
    """Serializer for FoodCategory model"""
    
    class Meta:
        model = FoodCategory
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    registered_by_username = serializers.CharField(source='registered_by.username', read_only=True)
    reserved_by_username = serializers.CharField(source='reserved_by.username', read_only=True, allow_null=True)
    is_expired_status = serializers.SerializerMethodField()
    compartment_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'description',
            'provider', 'provider_name', 'registered_by', 'registered_by_username',
            'status', 'product_type', 'quantity', 'unit',
            'original_price', 'discounted_price', 'discount_percentage', 'final_price',
            'required_temperature', 'temperature_min', 'temperature_max',
            'registration_date', 'expiration_date', 'expiration_alert_sent',
            'compartment', 'compartment_number', 'is_reserved', 'reserved_by',
            'reserved_by_username', 'reservation_date', 'image', 'notes',
            'is_expired_status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'registration_date', 'final_price', 'is_expired_status',
            'compartment_number', 'created_at', 'updated_at'
        ]
    
    def get_is_expired_status(self, obj):
        return obj.is_expired
    
    def get_compartment_number(self, obj):
        if obj.compartment:
            return obj.compartment.compartment_number
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Simplified serializer for product lists"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'provider_name', 'status',
            'product_type', 'quantity', 'unit', 'final_price',
            'expiration_date', 'is_reserved', 'image', 'created_at'
        ]
        read_only_fields = fields
    
    def get_final_price(self, obj):
        return str(obj.final_price) if obj.final_price else "0"


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new products"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'provider',
            'product_type', 'quantity', 'unit',
            'original_price', 'discounted_price', 'discount_percentage',
            'required_temperature', 'temperature_min', 'temperature_max',
            'expiration_date', 'compartment', 'image', 'notes'
        ]
    
    def create(self, validated_data):
        validated_data['registered_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating products"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'product_type', 'quantity',
            'original_price', 'discounted_price', 'discount_percentage',
            'required_temperature', 'temperature_min', 'temperature_max',
            'expiration_date', 'compartment', 'status', 'image', 'notes'
        ]


class ProductDetailSerializer(ProductSerializer):
    """Extended serializer with detailed information"""
    
    transactions = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()
    collections = serializers.SerializerMethodField()
    
    def get_transactions(self, obj):
        from apps.transactions.serializers import TransactionListSerializer
        transactions = obj.transactions.all()
        return TransactionListSerializer(transactions, many=True).data
    
    def get_reservations(self, obj):
        from apps.transactions.serializers import ReservationListSerializer
        reservations = obj.reservations.all()
        return ReservationListSerializer(reservations, many=True).data
    
    def get_collections(self, obj):
        from apps.transactions.serializers import CollectionListSerializer
        collections = obj.collections.all()
        return CollectionListSerializer(collections, many=True).data
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['transactions', 'reservations', 'collections']
