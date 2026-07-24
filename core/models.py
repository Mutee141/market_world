from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base: adds created_at / updated_at to any model that inherits it."""
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        abstract = True


class TenantModel(TimeStampedModel):
    """
    Abstract base class for every model that belongs to a specific store.
    Every tenant-scoped model (Product, Order, Customer, etc.) will inherit
    from this so it automatically gets a `store` FK + timestamps.
    """
    store = models.ForeignKey(
        'tenants.Store',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='%(class)ss',   # e.g. store.products, store.orders
    )

    class Meta:
        abstract = True