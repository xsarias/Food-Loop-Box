"""
Serializers for Authentication app
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from apps.authentication.models import AccessLog, UserPermission

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone',
            'document_id', 'document_type', 'role', 'password', 'password_confirm'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'document_id', 'document_type', 'role', 'is_verified',
            'profile_picture', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserDetailSerializer(UserSerializer):
    """Extended user serializer with permissions"""
    
    custom_permissions = serializers.SerializerMethodField()
    
    def get_custom_permissions(self, obj):
        permissions = obj.custom_permissions.all()
        return UserPermissionSerializer(permissions, many=True).data
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['custom_permissions']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user data"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'profile_picture'
        ]


class UserPermissionSerializer(serializers.ModelSerializer):
    """Serializer for UserPermission model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserPermission
        fields = [
            'id', 'user', 'user_username', 'permission_name', 'category',
            'can_view', 'can_edit', 'can_delete', 'can_export',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccessLogSerializer(serializers.ModelSerializer):
    """Serializer for AccessLog model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AccessLog
        fields = [
            'id', 'user', 'user_username', 'email', 'status', 'ip_address',
            'user_agent', 'failure_reason', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer for token generation with additional user data"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True, min_length=8)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        return data
