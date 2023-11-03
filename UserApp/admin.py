from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ['id', 'username', 'email', 'role']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # Remove 'first_name' and 'last_name'
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role',  'is_active', 'is_updated'),
        }),
    )


admin.site.register(UserProfile, CustomUserAdmin)
