from django.db import models
from core.models import TenantModel


class Payment(TenantModel):
    METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('cash', 'Cash (POS)'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
        ('card', 'Debit/Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('store_credit', 'Store Credit'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Gateway's transaction reference")
    gateway_response = models.JSONField(null=True, blank=True, help_text="Raw response stored for debugging/disputes")

    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.get_method_display()} - {self.status}"