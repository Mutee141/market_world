from django.db import models
from django.utils import timezone
from core.models import TenantModel
from catalog.models import ProductVariant


class Coupon(TenantModel):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('flat', 'Flat Amount'),
    )

    code = models.CharField(max_length=30)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # optional: restrict coupon to one category
    category = models.ForeignKey('catalog.Category', on_delete=models.SET_NULL, null=True, blank=True)

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Total times this coupon can be used, blank = unlimited")
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('store', 'code')

    def __str__(self):
        return self.code

    @property
    def is_valid_now(self):
        now = timezone.now()
        if not self.is_active or now < self.valid_from or now > self.valid_until:
            return False
        if self.usage_limit and self.times_used >= self.usage_limit:
            return False
        return True

    def calculate_discount(self, subtotal):
        if subtotal < self.min_order_amount:
            return 0
        if self.discount_type == 'percentage':
            discount = subtotal * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value
        return min(discount, subtotal)


class Cart(TenantModel):
    """
    One active cart per customer per store. For guest/anonymous shoppers
    (no login yet), we key the cart off a session_key instead of a customer.
    """
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, null=True, blank=True,
        related_name='carts'
    )
    session_key = models.CharField(max_length=100, blank=True, null=True, help_text="For guest carts before login")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    is_abandoned = models.BooleanField(default=False)
    checked_out_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['store', 'session_key'])]

    def __str__(self):
        return f"Cart #{self.id} ({self.customer or self.session_key})"

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def discount_amount(self):
        if self.coupon and self.coupon.is_valid_now:
            return self.coupon.calculate_discount(self.subtotal)
        return 0

    @property
    def total(self):
        return self.subtotal - self.discount_amount


class CartItem(TenantModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f"{self.variant} x{self.quantity}"

    @property
    def line_total(self):
        return self.variant.current_price * self.quantity