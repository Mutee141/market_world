from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'is_active', 'city')
    prepopulated_fields = {'slug': ('name',)}