from django.db import models
from core.models import TenantModel
from catalog.models import ProductVariant


class Branch(TenantModel):
    """A physical location of the store (e.g. HBK - Peshawar, HBK - Lahore)."""
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False, help_text="Main branch/warehouse")

    def __str__(self):
        return f"{self.name} ({self.city})"


class Stock(TenantModel):
    """
    Current stock quantity of a specific variant AT a specific branch.
    This is the single source of truth for 'how many do we have right now'.
    """
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stocks')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ('variant', 'branch')
        indexes = [models.Index(fields=['store', 'quantity'])]

    def __str__(self):
        return f"{self.variant} @ {self.branch.name}: {self.quantity}"

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold


class StockMovement(TenantModel):
    """
    Audit trail for every stock change — never mutate Stock.quantity directly
    from business logic; always create a StockMovement and let it update Stock
    (see inventory/services.py we'll add later). This gives you a full history
    for reports and disputes ('why did stock drop by 10 last Tuesday').
    """
    REASON_CHOICES = (
        ('purchase', 'Purchase / Received from supplier'),
        ('sale', 'Sale (order/POS)'),
        ('return', 'Customer Return'),
        ('transfer_in', 'Transfer In (from another branch)'),
        ('transfer_out', 'Transfer Out (to another branch)'),
        ('adjustment', 'Manual Adjustment'),
        ('damaged', 'Damaged/Expired'),
    )

    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='movements')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='movements')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    quantity_change = models.IntegerField(help_text="Positive = stock added, negative = stock removed")
    note = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    # optional links to the source document
    reference_id = models.CharField(max_length=64, blank=True, help_text="Order ID / PO ID / Transfer ID etc")

    class Meta:
        ordering = ['-created_at']


class Supplier(TenantModel):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PurchaseOrder(TenantModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('ordered', 'Ordered'),
        ('partially_received', 'Partially Received'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchase_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    reference_no = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"PO-{self.id} ({self.supplier.name})"

    @property
    def total_cost(self):
        return sum(item.quantity * item.unit_cost for item in self.items.all())


class PurchaseOrderItem(TenantModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='po_items')
    quantity = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_cost