from django.db import models
from django.utils.text import slugify
from core.models import TenantModel
from django.utils import timezone


class Category(TenantModel):
    """
    Supports nested categories: Electronics -> Mobiles -> Accessories.
    Scoped per store so each store builds its own category tree.
    """
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children'
    )
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order in menus")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ('store', 'slug')
        verbose_name_plural = 'categories'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(TenantModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('store', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TenantModel):
    """
    A product can be simple (no variants — e.g. a single kitchen knife) or
    have variants (a T-shirt in Small/Red, Large/Blue, etc.) — see
    ProductVariant below. Pricing/stock ALWAYS lives on the variant, even for
    simple products (which get exactly one auto-created 'default' variant).
    This keeps checkout/inventory logic uniform across the whole catalog.
    """

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tax_class = models.CharField(max_length=50, blank=True, help_text="Optional override of store default tax %")

    # searchable tags, comma separated for simplicity (e.g. "gift,new,sale")
    tags = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('store', 'slug')
        indexes = [models.Index(fields=['store', 'status'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(TenantModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ProductVariant(TenantModel):
    """
    e.g. Product='Nike Air Max' -> Variants: (Size=42,Color=Black), (Size=43,Color=White)
    For simple products, exactly one variant exists with attributes={}.
    SKU and barcode live here since POS/inventory scan at the variant level.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    sku = models.CharField(max_length=64)
    barcode = models.CharField(max_length=64, blank=True, null=True)

    # e.g. {"size": "42", "color": "Black"} — flexible, no separate attribute tables needed for v1
    attributes = models.JSONField(default=dict, blank=True)

    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    weight_kg = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('store', 'sku')
        indexes = [models.Index(fields=['store', 'barcode'])]

    def __str__(self):
        attrs = ', '.join(f"{k}:{v}" for k, v in self.attributes.items())
        return f"{self.product.name} ({attrs})" if attrs else self.product.name

    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.selling_price


class Review(TenantModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'customer')