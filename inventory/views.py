from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.viewsets import TenantScopedModelViewSet
from core.permissions import IsStoreStaff, IsOwnerOrManager
from .models import Branch, Stock, StockMovement, Supplier, PurchaseOrder
from .serializers import (
    BranchSerializer, StockSerializer, StockMovementSerializer,
    SupplierSerializer, PurchaseOrderSerializer
)


class BranchViewSet(TenantScopedModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsOwnerOrManager()]
        return [IsStoreStaff()]


class StockViewSet(TenantScopedModelViewSet):
    """Read + adjust only. quantity is never PATCHed directly — every change
    goes through /adjust/ so a StockMovement is always logged."""
    queryset = Stock.objects.select_related('variant', 'branch')
    serializer_class = StockSerializer
    filterset_fields = ['branch', 'variant']

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrManager])
    def adjust(self, request, pk=None):
        """Body: {"quantity_change": -3, "reason": "damaged", "note": "broken in transit"}"""
        stock = self.get_object()
        quantity_change = int(request.data.get('quantity_change', 0))
        reason = request.data.get('reason', 'adjustment')
        note = request.data.get('note', '')

        with transaction.atomic():
            new_qty = stock.quantity + quantity_change
            if new_qty < 0:
                return Response({'error': 'Adjustment would result in negative stock.'},
                                 status=status.HTTP_400_BAD_REQUEST)
            stock.quantity = new_qty
            stock.save(update_fields=['quantity'])
            StockMovement.objects.create(
                store=stock.store, variant=stock.variant, branch=stock.branch,
                reason=reason, quantity_change=quantity_change, note=note,
                performed_by=request.user,
            )
        return Response(StockSerializer(stock).data)


class StockMovementViewSet(TenantScopedModelViewSet):
    """Read-only — movements are created by services/actions, never directly."""
    queryset = StockMovement.objects.select_related('variant', 'branch')
    serializer_class = StockMovementSerializer
    filterset_fields = ['branch', 'variant', 'reason']
    http_method_names = ['get', 'head', 'options']


class SupplierViewSet(TenantScopedModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsOwnerOrManager]


class PurchaseOrderViewSet(TenantScopedModelViewSet):
    queryset = PurchaseOrder.objects.select_related('supplier', 'branch').prefetch_related('items')
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsOwnerOrManager]
    filterset_fields = ['status', 'supplier', 'branch']

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        """
        Marks a PO as received, adds stock, logs a 'purchase' StockMovement per item.
        Optional body: {"items": [{"item_id": 1, "quantity_received": 10}]}
        No body = receive full remaining quantity on every line item.
        """
        po = self.get_object()
        received_map = {i['item_id']: i['quantity_received'] for i in request.data.get('items', [])}

        with transaction.atomic():
            for item in po.items.all():
                qty = received_map.get(item.id, item.quantity - item.quantity_received)
                if qty <= 0:
                    continue

                item.quantity_received += qty
                item.save(update_fields=['quantity_received'])

                stock, _ = Stock.objects.select_for_update().get_or_create(
                    store=po.store, variant=item.variant, branch=po.branch,
                    defaults={'quantity': 0}
                )
                stock.quantity += qty
                stock.save(update_fields=['quantity'])

                StockMovement.objects.create(
                    store=po.store, variant=item.variant, branch=po.branch,
                    reason='purchase', quantity_change=qty,
                    reference_id=f"PO-{po.id}", performed_by=request.user,
                )

            all_received = all(i.quantity_received >= i.quantity for i in po.items.all())
            po.status = 'received' if all_received else 'partially_received'
            po.save(update_fields=['status'])

        return Response(PurchaseOrderSerializer(po).data)