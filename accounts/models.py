from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Shared user model for platform staff AND store staff.
    role + store together define what a user can see and do.
    """

    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Platform Super Admin'
        OWNER = 'owner', 'Store Owner'
        MANAGER = 'manager', 'Store Manager'
        CASHIER = 'cashier', 'Cashier / POS Operator'
        INVENTORY_STAFF = 'inventory_staff', 'Inventory Staff'
        SUPPORT = 'support', 'Support / Customer Service'
        CUSTOMER = 'customer', 'Customer'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    # Null for a platform super admin; set for every store-level user.
    store = models.ForeignKey(
        'tenants.Store', on_delete=models.CASCADE, null=True, blank=True,
        related_name='staff'
    )

    phone = models.CharField(max_length=20, blank=True)

    # Wired properly to inventory.Branch in Step 3 — plain int for now.
    branch_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_platform_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    def save(self, *args, **kwargs):
        if not self.store_id and not self.is_superuser:
            from tenants.models import Store
            store = Store.objects.filter(is_active=True).first()
            if store:
                self.store = store
        super().save(*args, **kwargs)