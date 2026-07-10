from django.contrib import admin

# Register your models here.
# users/admin.py

from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    """Custom admin for User model"""
    list_display = ('email', 'username', 'phone_number', 'is_active', 'email_verified')
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('-date_joined',)
    
    # The fields to show when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # The fields to show when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model"""
    list_display = ('user', 'fitness_goal', 'fitness_level', 'created_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('fitness_goal', 'fitness_level', 'gender')

# Register models with custom admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)