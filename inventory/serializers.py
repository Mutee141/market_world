from rest_framework import serializers
from .models import Branch, Stock, StockMovement, Supplier, PurchaseOrder, PurchaseOrderItem


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'city', 'phone', 'is_active', 'is_default']


class StockSerializer(serializers.ModelSerializer):
    variant_sku = serializers.CharField(source='variant.sku', read_only=True)
    product_name = serializers.CharField(source='variant.product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'variant', 'variant_sku', 'product_name', 'branch',
                  'branch_name', 'quantity', 'low_stock_threshold', 'is_low_stock']
        read_only_fields = ['quantity']  # quantity only changes via the /adjust/ action below


class StockMovementSerializer(serializers.ModelSerializer):
    variant_sku = serializers.CharField(source='variant.sku', read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'variant', 'variant_sku', 'branch', 'reason',
                  'quantity_change', 'note', 'reference_id', 'performed_by', 'created_at']
        read_only_fields = ['performed_by', 'created_at']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'phone', 'email', 'address', 'is_active']


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'variant', 'quantity', 'quantity_received', 'unit_cost']
        read_only_fields = ['quantity_received']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Nested-writable — create a PO with all its line items in one request."""
    items = PurchaseOrderItemSerializer(many=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    total_cost = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'supplier', 'supplier_name', 'branch', 'status',
                  'reference_no', 'notes', 'items', 'total_cost', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        store = self.context['request'].store
        po = PurchaseOrder.objects.create(store=store, **validated_data)
        for item in items_data:
            PurchaseOrderItem.objects.create(store=store, purchase_order=po, **item)
        return po

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                PurchaseOrderItem.objects.create(store=instance.store, purchase_order=instance, **item)
        return instance