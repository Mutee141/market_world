from rest_framework.routers import DefaultRouter
from .views import (
    BranchViewSet, StockViewSet, StockMovementViewSet,
    SupplierViewSet, PurchaseOrderViewSet
)

router = DefaultRouter()
router.register('branches', BranchViewSet, basename='branches')
router.register('stock', StockViewSet, basename='stock')
router.register('stock-movements', StockMovementViewSet, basename='stock-movements')
router.register('suppliers', SupplierViewSet, basename='suppliers')
router.register('purchase-orders', PurchaseOrderViewSet, basename='purchase-orders')

urlpatterns = router.urls