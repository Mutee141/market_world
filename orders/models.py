import uuid
from django.db import models
from core.models import TenantModel


class Order(TenantModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )

    SOURCE_CHOICES = (
        ('online', 'Online Storefront'),
    )

    order_number = models.CharField(max_length=30, unique=True, editable=False)

    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='orders')
    branch = models.ForeignKey('inventory.Branch', on_delete=models.PROTECT, related_name='orders', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='online')

    # Address snapshot — NOT a live FK to Address, because if the customer edits/deletes
    # their address later, past orders must still show what was shipped where at the time.
    shipping_address = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_phone = models.CharField(max_length=20, blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    coupon_code = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)

    placed_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders_placed', help_text="Cashier who rang this up, if POS"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['store', 'status'])]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def recalculate_totals(self):
        """Recomputes totals from line items — call after adding/editing items."""
        self.subtotal = sum(item.line_total for item in self.items.all())
        self.grand_total = self.subtotal - self.discount_amount + self.tax_amount + self.shipping_fee
        self.save(update_fields=['subtotal', 'grand_total'])


class OrderItem(TenantModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.PROTECT, related_name='order_items')

    # Snapshot the product name + price at time of sale — if the product is later
    # renamed/repriced, historical orders/invoices must stay accurate.
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


class OrderStatusHistory(TenantModel):
    """Audit trail every time an order's status changes — needed for order tracking UI."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    changed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['created_at']