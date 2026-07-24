from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, ProductViewSet, ProductVariantViewSet, ReviewViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('brands', BrandViewSet, basename='brands')
router.register('products', ProductViewSet, basename='products')
router.register('variants', ProductVariantViewSet, basename='variants')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = router.urls