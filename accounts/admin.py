from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Store Info', {'fields': ('role', 'store', 'phone', 'branch_id')}),
    )
    list_display = ('username', 'email', 'role', 'store', 'is_staff')
    list_filter = ('role', 'store', 'is_staff')