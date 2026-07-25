import os
from django.db import models
from django.utils.text import slugify
from core.models import TenantModel
from django.utils import timezone


def product_image_upload_to(instance, filename):
    """
    Saves uploaded product images into the 'products/' folder inside the project's media directory
    and automatically renames the image file directly to match the Product Title Name!
    Example: Product 'Wireless Gaming Headset' -> 'products/wireless-gaming-headset.jpg'
    If multiple images exist -> 'products/wireless-gaming-headset-2.jpg'
    """
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    
    product_name = ""
    if hasattr(instance, 'product') and instance.product and instance.product.name:
        product_name = instance.product.name
    elif hasattr(instance, 'name') and instance.name:
        product_name = instance.name
    else:
        product_name = "product"

    base_slug = slugify(product_name) or "product"
    
    order = getattr(instance, 'order', 1)
    if order and order > 1:
        new_filename = f"{base_slug}-{order}.{ext}"
    else:
        new_filename = f"{base_slug}.{ext}"

    return os.path.join('products', new_filename)


def category_image_upload_to(instance, filename):
    """
    Saves category images inside 'categories/' folder renamed directly to category title.
    """
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    name_slug = slugify(instance.name) if getattr(instance, 'name', None) else 'category'
    return os.path.join('categories', f"{name_slug}.{ext}")


def brand_logo_upload_to(instance, filename):
    """
    Saves brand logos inside 'brands/' folder renamed directly to brand title.
    """
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    name_slug = slugify(instance.name) if getattr(instance, 'name', None) else 'brand'
    return os.path.join('brands', f"{name_slug}-logo.{ext}")


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
    image = models.ImageField(upload_to=category_image_upload_to, blank=True, null=True)
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
    logo = models.ImageField(upload_to=brand_logo_upload_to, blank=True, null=True)
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
    image = models.ImageField(upload_to=product_image_upload_to)
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