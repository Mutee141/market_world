from django.db import models
from core.models import TimeStampedModel


class Store(TimeStampedModel):
    """A single tenant — one store/mall on the platform (e.g. HBK Hypermarket)."""

    STATUS_CHOICES = (
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, help_text="Used as subdomain: slug.yourplatform.com")
    custom_domain = models.CharField(max_length=255, blank=True, null=True, unique=True)

    owner = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='owned_stores'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    is_active = models.BooleanField(default=True)

    # branding — each store keeps its own identity
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='store_banners/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#0F172A')

    # contact / business info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # settings
    currency = models.CharField(max_length=3, default='PKR')
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name