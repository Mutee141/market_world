from django.contrib import admin



from django.contrib import admin
from .models import Customer, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'store', 'phone', 'is_guest', 'loyalty_points')
    list_filter = ('store', 'is_guest')
    search_fields = ('full_name', 'phone', 'email')
    inlines = [AddressInline]