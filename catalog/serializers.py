from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'image', 'is_active', 'order']
        read_only_fields = ['slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'is_active']
        read_only_fields = ['slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'order']


class ProductVariantSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku', 'barcode', 'attributes', 'cost_price',
                  'selling_price', 'discount_price', 'current_price', 'weight_kg', 'is_active']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight — used for catalog browsing / search result grids."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    price_from = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category_name', 'brand_name',
                  'status', 'primary_image', 'price_from']

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        return img.image.url if img else None

    def get_price_from(self, obj):
        variant = obj.variants.filter(is_active=True).order_by('selling_price').first()
        return variant.current_price if variant else None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full detail — product detail page + admin edit screen."""
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'category_name',
                  'brand', 'brand_name', 'status', 'tax_class', 'tags', 'images', 'variants']
        read_only_fields = ['slug']


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'customer', 'customer_name', 'rating', 'comment', 'is_approved']
        read_only_fields = ['customer']