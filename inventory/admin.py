from django.contrib import admin
from .models import Branch, Stock, StockMovement, Supplier, PurchaseOrder, PurchaseOrderItem


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'city', 'is_active', 'is_default')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('variant', 'branch', 'quantity', 'low_stock_threshold')
    list_filter = ('branch',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('variant', 'branch', 'reason', 'quantity_change', 'created_at')
    list_filter = ('reason', 'branch')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'phone', 'is_active')


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'branch', 'status', 'created_at')
    inlines = [PurchaseOrderItemInline]
    