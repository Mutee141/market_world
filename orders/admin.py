from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'store', 'customer', 'branch', 'status', 'source', 'grand_total', 'created_at')
    list_filter = ('store', 'status', 'source', 'branch')
    search_fields = ('order_number', 'customer__full_name', 'customer__phone')
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = ('order_number',)