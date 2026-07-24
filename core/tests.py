from django.contrib import admin
from django.test import SimpleTestCase

from carts.models import Cart
from catalog.models import Category
from customers.models import Customer
from inventory.models import InventoryItem
from orders.models import Order
from payments.models import Payment
from pos.models import POSSession


class AdminRegistrationTests(SimpleTestCase):
    def test_business_models_are_registered_in_admin(self):
        expected_models = [
            Category,
            InventoryItem,
            Customer,
            Order,
            Cart,
            Payment,
            POSSession,
        ]

        for model in expected_models:
            self.assertIn(model, admin.site._registry)
