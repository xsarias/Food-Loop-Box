"""
Serializers for Transactions app
"""

from rest_framework import serializers
from apps.transactions.models import Transaction, Reservation, Collection, DeviceInteraction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'buyer', 'buyer_username', 'product',
            'product_name', 'amount', 'currency', 'payment_method', 'status',
            'withdrawal_code', 'withdrawal_code_used', 'withdrawal_date',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'transaction_id', 'withdrawal_code', 'created_at', 'updated_at'
        ]


class TransactionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for transaction lists"""
    
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'buyer_username', 'product_name',
            'amount', 'payment_method', 'status', 'created_at'
        ]
        read_only_fields = fields


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating transactions"""
    
    class Meta:
        model = Transaction
        fields = [
            'product', 'amount', 'currency', 'payment_method', 'notes'
        ]
    
    def create(self, validated_data):
        import uuid
        validated_data['buyer'] = self.context['request'].user
        validated_data['transaction_id'] = f"TRX-{uuid.uuid4().hex[:12].upper()}"
        validated_data['withdrawal_code'] = f"WD-{uuid.uuid4().hex[:8].upper()}"
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer for Reservation model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_username', 'product', 'product_name',
            'status', 'reservation_date', 'expiration_date', 'collection_date',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'reservation_date', 'created_at', 'updated_at'
        ]


class ReservationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for reservation lists"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'user_username', 'product_name', 'status',
            'reservation_date', 'expiration_date', 'collection_date'
        ]
        read_only_fields = fields


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reservations"""
    
    class Meta:
        model = Reservation
        fields = ['product', 'expiration_date', 'notes']
    
    def create(self, validated_data):
        from datetime import timedelta
        validated_data['user'] = self.context['request'].user
        if not validated_data.get('expiration_date'):
            from django.utils import timezone
            validated_data['expiration_date'] = timezone.now() + timedelta(days=3)
        return super().create(validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    """Serializer for Collection model"""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    collected_by_username = serializers.CharField(source='collected_by.username', read_only=True, allow_null=True)
    device_name = serializers.CharField(source='device.device_id', read_only=True, allow_null=True)
    
    class Meta:
        model = Collection
        fields = [
            'id', 'product', 'product_name', 'collected_by', 'collected_by_username',
            'status', 'device', 'device_name', 'scheduled_date', 'actual_collection_date',
            'withdrawal_code', 'code_verified', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]


class CollectionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for collection lists"""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Collection
        fields = [
            'id', 'product_name', 'status', 'scheduled_date',
            'actual_collection_date', 'code_verified'
        ]
        read_only_fields = fields


class DeviceInteractionSerializer(serializers.ModelSerializer):
    """Serializer for DeviceInteraction model"""
    
    device_name = serializers.CharField(source='device.device_id', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = DeviceInteraction
        fields = [
            'id', 'device', 'device_name', 'user', 'user_username',
            'interaction_type', 'success', 'error_message', 'withdrawal_code',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class DeviceInteractionLogSerializer(serializers.ModelSerializer):
    """Serializer for device interaction logs"""
    
    device_name = serializers.CharField(source='device.device_id', read_only=True)
    
    class Meta:
        model = DeviceInteraction
        fields = [
            'id', 'device_name', 'interaction_type', 'success',
            'error_message', 'timestamp'
        ]
        read_only_fields = fields
