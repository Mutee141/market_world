from django.db import models
from core.models import TenantModel


class Customer(TenantModel):
    """
    A customer belongs to ONE store (per our earlier decision — not shared
    across stores). Can optionally be linked to a login User account for
    online shopping, OR exist standalone for walk-in POS customers who never
    create an account.
    """
    user = models.OneToOneField(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='customer_profile'
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    # Loyalty / segmentation
    loyalty_points = models.PositiveIntegerField(default=0)
    store_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    is_guest = models.BooleanField(default=False, help_text="True for walk-in/POS-only customers with no login")

    class Meta:
        indexes = [models.Index(fields=['store', 'phone'])]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    @property
    def total_orders(self):
        return self.orders.count()

    @property
    def total_spent(self):
        from django.db.models import Sum
        result = self.orders.filter(status='delivered').aggregate(total=Sum('grand_total'))
        return result['total'] or 0


class Address(TenantModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=50, blank=True, help_text="e.g. Home, Office")
    full_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label or 'Address'} - {self.city}"