"""
Admin configuration for Authentication app
"""

from django.contrib import admin
from apps.authentication.models import User, AccessLog, UserPermission


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'document_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'first_name', 'last_name', 'email')
        }),
        ('Contact', {
            'fields': ('phone',)
        }),
        ('Document', {
            'fields': ('document_type', 'document_id')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_staff', 'is_superuser', 'groups')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Status', {
            'fields': ('is_active', 'last_login')
        }),
        ('Profile', {
            'fields': ('profile_picture',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'ip_address', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('email', 'ip_address', 'user__username')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('Access Information', {
            'fields': ('user', 'email', 'status')
        }),
        ('Connection', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Details', {
            'fields': ('failure_reason',)
        }),
        ('Metadata', {
            'fields': ('timestamp',)
        }),
    )


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission_name', 'category', 'can_view', 'can_edit', 'created_at')
    list_filter = ('category', 'can_view', 'can_edit', 'can_delete', 'created_at')
    search_fields = ('user__username', 'permission_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User & Permission', {
            'fields': ('user', 'permission_name', 'category')
        }),
        ('Permissions', {
            'fields': ('can_view', 'can_edit', 'can_delete', 'can_export')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
