import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tenants.models import Store
from catalog.models import Category, Brand, Product, ProductVariant, Review, ProductImage
from inventory.models import Branch, Stock
from customers.models import Customer

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with dynamic Electro Bootstrap store data"

    def handle(self, *args, **options):
        self.stdout.write("Cleaning other stores...")
        from catalog.models import Product, Category, Brand
        Product.objects.exclude(store__slug="electro").delete()
        Category.objects.exclude(store__slug="electro").delete()
        Brand.objects.exclude(store__slug="electro").delete()
        Store.objects.exclude(slug="electro").delete()
        self.stdout.write("Seeding data...")

        # 2. Create Owner User
        owner, created = User.objects.get_or_create(
            username="electro_owner",
            defaults={
                "email": "owner@electroworld.com",
                "role": User.Role.OWNER,
                "phone": "+123456789"
            }
        )
        if created:
            owner.set_password("password123")
            owner.save()

        # 3. Create Store
        store, _ = Store.objects.get_or_create(
            slug="electro",
            defaults={
                "name": "Electro World",
                "owner": owner,
                "currency": "PKR",
                "tax_percentage": 5.00,
                "phone": "+1234567890",
                "email": "info@electroworld.com",
                "address": "123 Electronic Street",
                "city": "New York"
            }
        )

        # Update owner's store
        owner.store = store
        owner.save()

        # 4. Create Branches
        main_branch, _ = Branch.objects.get_or_create(
            store=store,
            name="Main Warehouse",
            defaults={
                "address": "456 Storage Blvd",
                "city": "New York",
                "phone": "+1999888777",
                "is_default": True
            }
        )
        downtown_branch, _ = Branch.objects.get_or_create(
            store=store,
            name="Downtown Store",
            defaults={
                "address": "789 Broadway",
                "city": "New York",
                "phone": "+1888777666",
                "is_default": False
            }
        )

        # 5. Create Categories
        electronics, _ = Category.objects.get_or_create(
            store=store,
            name="Electronics",
            defaults={"order": 1}
        )
        laptops, _ = Category.objects.get_or_create(
            store=store,
            name="Laptops",
            defaults={"parent": electronics, "order": 2}
        )
        smartphones, _ = Category.objects.get_or_create(
            store=store,
            name="Smartphones",
            defaults={"parent": electronics, "order": 3}
        )
        tvs, _ = Category.objects.get_or_create(
            store=store,
            name="Televisions",
            defaults={"parent": electronics, "order": 4}
        )
        accessories, _ = Category.objects.get_or_create(
            store=store,
            name="Accessories",
            defaults={"parent": electronics, "order": 5}
        )

        # 6. Create Brands
        apple, _ = Brand.objects.get_or_create(store=store, name="Apple")
        samsung, _ = Brand.objects.get_or_create(store=store, name="Samsung")
        dell, _ = Brand.objects.get_or_create(store=store, name="Dell")
        sony, _ = Brand.objects.get_or_create(store=store, name="Sony")

        # 7. Products, Variants & Stocks List
        product_data = [
            {
                "category": laptops,
                "brand": dell,
                "name": "Dell XPS 15",
                "description": "Premium 15-inch laptop with stunning InfinityEdge display, 13th Gen Intel Core processors, and sleek design.",
                "tags": "laptop,dell,xps,workstation",
                "variants": [
                    {
                        "sku": "DELL-XPS15-I7",
                        "attributes": {"CPU": "Intel i7", "RAM": "16GB", "SSD": "512GB"},
                        "cost_price": 1000.00,
                        "selling_price": 1499.99,
                        "discount_price": 1399.99,
                        "stocks": [(main_branch, 15), (downtown_branch, 5)]
                    },
                    {
                        "sku": "DELL-XPS15-I9",
                        "attributes": {"CPU": "Intel i9", "RAM": "32GB", "SSD": "1TB"},
                        "cost_price": 1400.00,
                        "selling_price": 1999.99,
                        "discount_price": None,
                        "stocks": [(main_branch, 8), (downtown_branch, 2)]  # Low stock in downtown
                    }
                ],
                "mock_image_index": 1
            },
            {
                "category": smartphones,
                "brand": apple,
                "name": "iPhone 15 Pro",
                "description": "Featuring a strong and light titanium design, a new Action button, powerful camera system, and the A17 Pro chip.",
                "tags": "iphone,apple,ios,smartphone",
                "variants": [
                    {
                        "sku": "IPHONE-15P-128GB",
                        "attributes": {"Storage": "128GB", "Color": "Titanium Gray"},
                        "cost_price": 700.00,
                        "selling_price": 1099.99,
                        "discount_price": 999.99,
                        "stocks": [(main_branch, 20), (downtown_branch, 10)]
                    },
                    {
                        "sku": "IPHONE-15P-256GB",
                        "attributes": {"Storage": "256GB", "Color": "Space Black"},
                        "cost_price": 800.00,
                        "selling_price": 1199.99,
                        "discount_price": None,
                        "stocks": [(main_branch, 12), (downtown_branch, 3)]
                    }
                ],
                "mock_image_index": 2
            },
            {
                "category": smartphones,
                "brand": samsung,
                "name": "Samsung Galaxy S24 Ultra",
                "description": "The ultimate smartphone experience. Built-in S Pen, advanced nightography camera system, and all-day power with Snapdragon 8 Gen 3.",
                "tags": "samsung,galaxy,android,smartphone",
                "variants": [
                    {
                        "sku": "SAMSUNG-S24U",
                        "attributes": {"Storage": "256GB", "Color": "Titanium Yellow"},
                        "cost_price": 800.00,
                        "selling_price": 1299.99,
                        "discount_price": 1199.99,
                        "stocks": [(main_branch, 25), (downtown_branch, 12)]
                    }
                ],
                "mock_image_index": 3
            },
            {
                "category": tvs,
                "brand": sony,
                "name": "Sony Bravia 65-Inch 4K TV",
                "description": "Smart Google TV with breathtaking 4K HDR processor, deep contrast, immersive audio, and seamless gaming integrations.",
                "tags": "sony,bravia,tv,smart-tv,4k",
                "variants": [
                    {
                        "sku": "SONY-BR65",
                        "attributes": {"Size": "65-Inch", "Resolution": "4K UHD"},
                        "cost_price": 500.00,
                        "selling_price": 899.99,
                        "discount_price": 799.99,
                        "stocks": [(main_branch, 10), (downtown_branch, 4)]
                    }
                ],
                "mock_image_index": 4
            },
            {
                "category": accessories,
                "brand": apple,
                "name": "Apple AirPods Pro 2",
                "description": "Active Noise Cancellation, adaptive transparency mode, personalized spatial audio, and sweat/water resistance.",
                "tags": "apple,airpods,audio,earphones",
                "variants": [
                    {
                        "sku": "APPLE-AP2",
                        "attributes": {"Generation": "2nd Gen"},
                        "cost_price": 130.00,
                        "selling_price": 249.99,
                        "discount_price": 219.99,
                        "stocks": [(main_branch, 50), (downtown_branch, 20)]
                    }
                ],
                "mock_image_index": 5
            },
            {
                "category": accessories,
                "brand": samsung,
                "name": "Samsung Galaxy Watch 6",
                "description": "Track your fitness, health metrics, and sleep quality. Sleek design, custom watch faces, and LTE connectivity.",
                "tags": "samsung,watch,wearable,smartwatch",
                "variants": [
                    {
                        "sku": "SAMSUNG-WATCH6",
                        "attributes": {"Size": "44mm", "Color": "Graphite"},
                        "cost_price": 180.00,
                        "selling_price": 299.99,
                        "discount_price": None,
                        "stocks": [(main_branch, 30), (downtown_branch, 8)]
                    }
                ],
                "mock_image_index": 6
            }
        ]

        for p_info in product_data:
            # Create product
            prod, _ = Product.objects.get_or_create(
                store=store,
                name=p_info["name"],
                defaults={
                    "category": p_info["category"],
                    "brand": p_info["brand"],
                    "description": p_info["description"],
                    "status": "active",
                    "tags": p_info["tags"]
                }
            )

            # Create default primary image record (we point it to a logical static path or name)
            ProductImage.objects.get_or_create(
                store=store,
                product=prod,
                is_primary=True,
                defaults={
                    "image": f"product-{p_info['mock_image_index']}.png",
                    "order": 1
                }
            )

            # Create variants & stock levels
            for v_info in p_info["variants"]:
                variant, _ = ProductVariant.objects.get_or_create(
                    store=store,
                    sku=v_info["sku"],
                    defaults={
                        "product": prod,
                        "attributes": v_info["attributes"],
                        "cost_price": v_info["cost_price"],
                        "selling_price": v_info["selling_price"],
                        "discount_price": v_info["discount_price"],
                        "is_active": True
                    }
                )

                # Set Stock at branches
                for branch, qty in v_info["stocks"]:
                    Stock.objects.update_or_create(
                        store=store,
                        variant=variant,
                        branch=branch,
                        defaults={
                            "quantity": qty,
                            "low_stock_threshold": 5
                        }
                    )

        # 8. Create Customer Profile for reviews/purchases
        cust, _ = Customer.objects.get_or_create(
            store=store,
            phone="+1231231234",
            defaults={
                "full_name": "John Doe",
                "email": "johndoe@test.com",
                "loyalty_points": 120,
                "store_credit": 0.00
            }
        )

        # 9. Create Product Reviews
        xps = Product.objects.get(store=store, name="Dell XPS 15")
        Review.objects.get_or_create(
            store=store,
            product=xps,
            customer=cust,
            defaults={
                "rating": 5,
                "comment": "Absolutely love the screen and processing power! Highly recommend.",
                "is_approved": True
            }
        )

        iphone = Product.objects.get(store=store, name="iPhone 15 Pro")
        Review.objects.get_or_create(
            store=store,
            product=iphone,
            customer=cust,
            defaults={
                "rating": 4,
                "comment": "Solid titanium build feels great, battery life is good, not a massive upgrade from 14 but worth it.",
                "is_approved": True
            }
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with Electro World data!"))
