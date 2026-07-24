from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.viewsets import TenantScopedModelViewSet
from core.permissions import IsStoreStaff, IsOwnerOrManager
from .models import Category, Brand, Product, ProductVariant, Review
from .serializers import (
    CategorySerializer, BrandSerializer, ProductListSerializer,
    ProductDetailSerializer, ProductVariantSerializer, ReviewSerializer
)


class CategoryViewSet(TenantScopedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['parent', 'is_active']


class BrandViewSet(TenantScopedModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_fields = ['is_active']


class ProductViewSet(TenantScopedModelViewSet):
    """
    Powers BOTH the admin product screen and public storefront browsing —
    same tenant-scoped endpoint. Only write actions are role-restricted.
    """
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('images', 'variants')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'brand', 'status']
    search_fields = ['name', 'tags']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        return ProductListSerializer if self.action == 'list' else ProductDetailSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsOwnerOrManager()]
        return [IsStoreStaff()]


class ProductVariantViewSet(TenantScopedModelViewSet):
    queryset = ProductVariant.objects.select_related('product')
    serializer_class = ProductVariantSerializer
    filterset_fields = ['product', 'is_active']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsOwnerOrManager()]
        return [IsStoreStaff()]


class ReviewViewSet(TenantScopedModelViewSet):
    queryset = Review.objects.select_related('customer', 'product')
    serializer_class = ReviewSerializer
    filterset_fields = ['product', 'is_approved']