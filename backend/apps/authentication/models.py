"""
Authentication models for Food Loop Box application
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    """Extended User model with additional fields"""
    
    USER_ROLES = [
        ('admin', 'Administrador'),
        ('partner', 'Aliado'),
        ('customer', 'Cliente'),
        ('driver', 'Conductor'),
        ('support', 'Soporte'),
    ]
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    phone = models.CharField(max_length=20, blank=True)
    document_id = models.CharField(max_length=50, blank=True, unique=True)
    document_type = models.CharField(max_length=20, choices=[('cc', 'Cédula'), ('passport', 'Pasaporte')], default='cc', blank=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"


class AccessLog(models.Model):
    """Audit trail for user access attempts"""
    
    ACCESS_STATUS = [
        ('success', 'Éxito'),
        ('failure', 'Fallido'),
        ('blocked', 'Bloqueado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='access_logs')
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=ACCESS_STATUS)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    failure_reason = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Access Log"
        verbose_name_plural = "Access Logs"
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['email', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.status} - {self.timestamp}"


class UserPermission(models.Model):
    """Custom permissions for users"""
    
    PERMISSION_CATEGORIES = [
        ('products', 'Productos'),
        ('transactions', 'Transacciones'),
        ('analytics', 'Análisis'),
        ('device_management', 'Gestión de Dispositivos'),
        ('user_management', 'Gestión de Usuarios'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_permissions')
    permission_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=PERMISSION_CATEGORIES)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user', 'category']
        unique_together = ['user', 'permission_name']
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"
    
    def __str__(self):
        return f"{self.user.username} - {self.permission_name}"
