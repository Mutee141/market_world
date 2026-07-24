import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test.client import Client
from rest_framework.test import APIClient
from tenants.models import Store
from accounts.models import User

def run_tests():
    print("Clearing database for single-store validation...")
    from catalog.models import Product, Category, Brand
    Product.objects.all().delete()
    Category.objects.all().delete()
    Brand.objects.all().delete()
    Store.objects.all().delete()
    User.objects.all().delete()
    
    print("Setting up single test store and user...")
    
    # Setup the single Store
    store1 = Store.objects.create(name='HBK', slug='hbk')
    
    # Setup store owner
    owner1 = User.objects.create_user(
        username='your_owner_username',
        email='owner1@test.com',
        password='yourpassword',
        role='owner',
        store=store1
    )

    client = APIClient()

    print("\n--- Test 1: Log in as Owner ---")
    response = client.post('/api/auth/login/', {'username': 'your_owner_username', 'password': 'yourpassword'}, format='json')
    if response.status_code == 200:
        access_token_1 = response.data.get('access')
        print("SUCCESS: Logged in. Token retrieved.")
    else:
        print("FAILED: Login failed.", response.status_code, response.data)
        return

    print("\n--- Test 2: List products for the store ---")
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token_1)
    response = client.get('/api/catalog/products/')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")

    print("\n--- Test 3: Create a category ---")
    response = client.post('/api/catalog/categories/', {'name': 'Electronics'}, format='json')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")

    # To check stock adjustment, we need to create a product, variant, branch, and stock entry
    print("\n--- Test 4: Setup stock and run adjustment ---")
    from catalog.models import Category, Product, ProductVariant
    from inventory.models import Branch, Stock
    
    category = Category.objects.filter(store=store1).first()
    product = Product.objects.create(store=store1, name='Test Phone', category=category, status='active')
    variant = ProductVariant.objects.create(store=store1, product=product, sku='TEST-SKU', selling_price=100)
    branch = Branch.objects.create(store=store1, name='Test Branch')
    stock = Stock.objects.create(store=store1, variant=variant, branch=branch, quantity=10)
    
    response = client.post(f'/api/inventory/stock/{stock.id}/adjust/', {'quantity_change': -5, 'reason': 'damaged', 'note': 'test adjustment'}, format='json')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")

if __name__ == '__main__':
    run_tests()
