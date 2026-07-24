from django.contrib import admin
from .models import Coupon, Cart, CartItem


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'store', 'discount_type', 'discount_value', 'is_active', 'times_used')
    list_filter = ('store', 'is_active')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'customer', 'is_abandoned', 'created_at')
    list_filter = ('store', 'is_abandoned')
    inlines = [CartItemInline]