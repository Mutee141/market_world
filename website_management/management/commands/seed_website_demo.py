"""
Management command: seed_website_demo
Seeds all Website Management sections with realistic demo content.
Run once per store to populate slides, banners, menus, and pages.
"""
from django.core.management.base import BaseCommand
from tenants.models import Store
from website_management.models import (
    HeroSlide, PromotionalBanner, MenuItem, Page,
    HomepageSection, SiteSettings, MediaFile
)


class Command(BaseCommand):
    help = 'Seed demo content for Website Management (slides, banners, menus, pages) for all stores.'

    def add_arguments(self, parser):
        parser.add_argument('--store', type=str, default=None, help='Seed only for a specific store domain')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        stores = Store.objects.all()
        if options['store']:
            stores = stores.filter(domain=options['store'])

        for store in stores:
            self.stdout.write(f'\n📦 Seeding demo content for: {store.name}')

            if options['clear']:
                HeroSlide.objects.filter(store=store).delete()
                PromotionalBanner.objects.filter(store=store).delete()
                MenuItem.objects.filter(store=store).delete()
                Page.objects.filter(store=store).delete()
                HomepageSection.objects.filter(store=store).delete()
                self.stdout.write('   🗑  Cleared existing content.')

            self._seed_hero_slides(store)
            self._seed_banners(store)
            self._seed_menus(store)
            self._seed_pages(store)
            self._seed_homepage_sections(store)
            self._seed_site_settings(store)

            self.stdout.write(self.style.SUCCESS(f'   ✅ Done seeding {store.name}'))

    def _seed_hero_slides(self, store):
        if HeroSlide.objects.filter(store=store).exists():
            self.stdout.write('   ⏭  Hero slides already exist, skipping.')
            return

        slides = [
            {
                'title': 'New Arrivals — Electronics',
                'subtitle': 'Discover the latest tech at unbeatable prices. Shop smartphones, laptops, and accessories.',
                'badge': '🔥 NEW',
                'button_text': 'Shop Now',
                'button_link': '/shop/',
                'image': 'hero_slides/demo_slide_electronics.png',
                'display_order': 1,
                'text_color': '#ffffff',
                'text_alignment': 'left',
                'overlay_enabled': True,
                'animation_type': 'fade',
                'alt_text': 'Electronics New Arrivals hero banner',
            },
            {
                'title': 'Summer Collection 2025',
                'subtitle': 'Style meets comfort. Explore our premium fashion lineup for every occasion.',
                'badge': '✨ TRENDING',
                'button_text': 'Explore Collection',
                'button_link': '/shop/?category=fashion',
                'image': 'hero_slides/demo_slide_fashion.png',
                'display_order': 2,
                'text_color': '#ffffff',
                'text_alignment': 'center',
                'overlay_enabled': True,
                'animation_type': 'slide',
                'alt_text': 'Summer fashion collection hero banner',
            },
        ]

        for data in slides:
            HeroSlide.objects.create(store=store, **data)

        self.stdout.write(f'   🖼  Added {len(slides)} hero slides.')

    def _seed_banners(self, store):
        if PromotionalBanner.objects.filter(store=store).exists():
            self.stdout.write('   ⏭  Promotional banners already exist, skipping.')
            return

        banners = [
            {
                'title': '⚡ Flash Sale',
                'subtitle': 'Up to 70% OFF — Limited time only!',
                'button_text': 'Grab Deals',
                'button_link': '/shop/?tag=sale',
                'position': 'home_top',
                'display_order': 1,
                'image': 'banners/demo_banner_flash_sale.png',
                'background_color': '#dc3545',
                'text_color': '#ffffff',
                'alt_text': 'Flash sale promotional banner',
            },
            {
                'title': '🕌 Eid Special Offers',
                'subtitle': 'Celebrate Eid with exclusive gifts and savings on top brands',
                'button_text': 'Shop Eid Deals',
                'button_link': '/shop/?q=eid',
                'position': 'home_middle',
                'display_order': 1,
                'image': 'banners/demo_banner_eid.png',
                'background_color': '#155724',
                'text_color': '#ffffff',
                'alt_text': 'Eid special sale banner',
            },
            {
                'title': '🚚 Free Delivery',
                'subtitle': 'Free delivery on all orders over Rs. 5,000. Order now!',
                'button_text': 'Order Now',
                'button_link': '/shop/',
                'position': 'home_bottom',
                'display_order': 1,
                'image': 'banners/demo_banner_delivery.png',
                'background_color': '#0d6efd',
                'text_color': '#ffffff',
                'alt_text': 'Free delivery promotional banner',
            },
            {
                'title': '🛍 Category Deals',
                'subtitle': 'Exclusive offers on all categories this week',
                'button_text': 'View All',
                'button_link': '/shop/',
                'position': 'category_page',
                'display_order': 1,
                'image': 'banners/demo_banner_flash_sale.png',
                'background_color': '#6f42c1',
                'text_color': '#ffffff',
                'alt_text': 'Category page deals banner',
            },
        ]

        for data in banners:
            PromotionalBanner.objects.create(store=store, **data)

        self.stdout.write(f'   📢  Added {len(banners)} promotional banners.')

    def _seed_menus(self, store):
        if MenuItem.objects.filter(store=store).exists():
            self.stdout.write('   ⏭  Menu items already exist, skipping.')
            return

        # Header Navigation
        header_items = [
            {'label': 'Home',        'url': '/',             'location': 'header', 'icon': 'fa-home',         'display_order': 1},
            {'label': 'Shop',        'url': '/shop/',        'location': 'header', 'icon': 'fa-store',        'display_order': 2},
            {'label': 'New Arrivals','url': '/shop/?tag=new','location': 'header', 'icon': 'fa-star',         'display_order': 3},
            {'label': 'Sale',        'url': '/shop/?tag=sale','location':'header', 'icon': 'fa-percent',      'display_order': 4},
            {'label': 'Contact',     'url': '/contact/',     'location': 'header', 'icon': 'fa-envelope',     'display_order': 5},
        ]

        # Footer Navigation
        footer_items = [
            {'label': 'About Us',    'url': '/pages/about-us/',   'location': 'footer', 'display_order': 1},
            {'label': 'Privacy Policy','url':'/pages/privacy-policy/','location':'footer','display_order':2},
            {'label': 'Terms of Service','url':'/pages/terms-of-service/','location':'footer','display_order':3},
            {'label': 'Refund Policy','url':'/pages/refund-policy/', 'location':'footer','display_order':4},
            {'label': 'FAQ',         'url': '/pages/faq/',        'location': 'footer', 'display_order': 5},
            {'label': 'Shipping Info','url':'/pages/shipping/',   'location': 'footer', 'display_order': 6},
        ]

        # Mega Menu
        mega_items = [
            {'label': 'Electronics', 'url': '/shop/?category=electronics', 'location': 'mega_menu', 'icon': 'fa-laptop',    'display_order': 1},
            {'label': 'Fashion',     'url': '/shop/?category=fashion',     'location': 'mega_menu', 'icon': 'fa-tshirt',    'display_order': 2},
            {'label': 'Sports',      'url': '/shop/?category=sports',      'location': 'mega_menu', 'icon': 'fa-football',  'display_order': 3},
            {'label': 'Home & Living','url':'/shop/?category=home',        'location': 'mega_menu', 'icon': 'fa-couch',     'display_order': 4},
            {'label': 'Beauty',      'url': '/shop/?category=beauty',      'location': 'mega_menu', 'icon': 'fa-gem',       'display_order': 5},
        ]

        all_items = header_items + footer_items + mega_items
        for data in all_items:
            MenuItem.objects.create(store=store, **data)

        self.stdout.write(f'   🗂  Added {len(all_items)} menu items (header + footer + mega menu).')

    def _seed_pages(self, store):
        if Page.objects.filter(store=store).exists():
            self.stdout.write('   ⏭  Pages already exist, skipping.')
            return

        pages = [
            {
                'title': 'About Us',
                'slug': 'about-us',
                'status': 'published',
                'display_order': 1,
                'show_in_footer': True,
                'seo_title': 'About Us — Our Story & Mission',
                'seo_description': 'Learn about our store, our team, and our commitment to bringing you the best products.',
                'content': """<h2>Our Story</h2>
<p>Founded with a passion for quality and value, we are dedicated to delivering the best products to your doorstep. Our journey began with a simple idea: make premium products accessible to everyone.</p>

<h3>Our Mission</h3>
<p>We believe shopping should be simple, affordable, and enjoyable. That's why we carefully curate every product in our catalog to ensure exceptional quality and value.</p>

<h3>Why Choose Us?</h3>
<ul>
  <li>✅ Thousands of verified products</li>
  <li>✅ Fast nationwide delivery</li>
  <li>✅ Secure payment methods</li>
  <li>✅ 7-day easy returns</li>
  <li>✅ 24/7 customer support</li>
</ul>

<h3>Our Team</h3>
<p>We are a passionate team of professionals dedicated to bringing you the best shopping experience. From our buying team that selects quality products, to our customer care agents ready to help — we work as one to serve you better.</p>"""
            },
            {
                'title': 'Privacy Policy',
                'slug': 'privacy-policy',
                'status': 'published',
                'display_order': 2,
                'show_in_footer': True,
                'seo_title': 'Privacy Policy — How We Use Your Data',
                'seo_description': 'Our privacy policy explains how we collect, use, and protect your personal information.',
                'content': """<h2>Privacy Policy</h2>
<p>Last updated: January 2025</p>

<h3>1. Information We Collect</h3>
<p>We collect information you provide directly, such as your name, email address, phone number, and shipping address when you place an order or create an account.</p>

<h3>2. How We Use Your Information</h3>
<ul>
  <li>To process and fulfill your orders</li>
  <li>To communicate about your order status</li>
  <li>To improve our services and website</li>
  <li>To send promotional offers (with your consent)</li>
</ul>

<h3>3. Data Security</h3>
<p>We implement industry-standard security measures to protect your personal information. Your payment information is encrypted and never stored on our servers.</p>

<h3>4. Contact Us</h3>
<p>For privacy-related queries, contact our Data Protection Officer at privacy@yourstore.com</p>"""
            },
            {
                'title': 'Terms of Service',
                'slug': 'terms-of-service',
                'status': 'published',
                'display_order': 3,
                'show_in_footer': True,
                'seo_title': 'Terms of Service — Usage Agreement',
                'seo_description': 'Read our terms of service before using our platform.',
                'content': """<h2>Terms of Service</h2>
<p>By using our website, you agree to these terms. Please read carefully.</p>

<h3>1. Acceptance of Terms</h3>
<p>By accessing and using this website, you accept and agree to be bound by these Terms of Service.</p>

<h3>2. Products & Pricing</h3>
<p>We reserve the right to modify prices at any time. All prices are in PKR and inclusive of applicable taxes unless stated otherwise.</p>

<h3>3. Orders & Payment</h3>
<p>Orders are confirmed only after successful payment or Cash on Delivery confirmation. We reserve the right to cancel orders due to stock availability or pricing errors.</p>

<h3>4. Limitation of Liability</h3>
<p>Our liability is limited to the purchase price of the product. We are not responsible for indirect damages arising from product use.</p>"""
            },
            {
                'title': 'Refund Policy',
                'slug': 'refund-policy',
                'status': 'published',
                'display_order': 4,
                'show_in_footer': True,
                'seo_title': 'Refund & Return Policy — 7 Day Easy Returns',
                'seo_description': 'Understand our hassle-free 7-day return and refund policy.',
                'content': """<h2>Refund & Return Policy</h2>

<h3>7-Day Return Policy</h3>
<p>We offer a 7-day return window from the date of delivery. Items must be unused, in original packaging, and accompanied by the original receipt.</p>

<h3>How to Initiate a Return</h3>
<ol>
  <li>Contact our support team within 7 days of delivery</li>
  <li>Provide your order number and reason for return</li>
  <li>Our team will arrange a pickup or guide you on drop-off</li>
  <li>Refund is processed within 5-7 business days of receiving the item</li>
</ol>

<h3>Non-Returnable Items</h3>
<ul>
  <li>Opened software or digital products</li>
  <li>Perishable goods</li>
  <li>Items marked as "Final Sale"</li>
  <li>Undergarments for hygiene reasons</li>
</ul>

<h3>Refund Methods</h3>
<p>Refunds are processed to the original payment method. Cash on Delivery orders are refunded via bank transfer.</p>"""
            },
            {
                'title': 'FAQ',
                'slug': 'faq',
                'status': 'published',
                'display_order': 5,
                'show_in_footer': True,
                'seo_title': 'Frequently Asked Questions',
                'seo_description': 'Get answers to common questions about orders, delivery, payments, and returns.',
                'content': """<h2>Frequently Asked Questions</h2>

<h3>📦 Orders & Delivery</h3>

<p><strong>How long does delivery take?</strong><br>
Standard delivery takes 3-5 business days. Express delivery is available in 1-2 days for major cities.</p>

<p><strong>Do you deliver nationwide?</strong><br>
Yes, we deliver to all major cities and towns across Pakistan.</p>

<p><strong>How do I track my order?</strong><br>
Once your order is dispatched, you will receive an SMS/email with a tracking link.</p>

<h3>💳 Payments</h3>

<p><strong>What payment methods do you accept?</strong><br>
We accept Cash on Delivery (COD) and bank transfers. Online card payments coming soon!</p>

<p><strong>Is Cash on Delivery available everywhere?</strong><br>
COD is available in most cities. You'll see COD availability at checkout for your area.</p>

<h3>🔄 Returns & Refunds</h3>

<p><strong>How do I return a product?</strong><br>
Contact us within 7 days of receiving your order. See our full Return Policy for details.</p>

<p><strong>When will I receive my refund?</strong><br>
Refunds are processed within 5-7 business days after we receive the returned item.</p>"""
            },
            {
                'title': 'Shipping Information',
                'slug': 'shipping',
                'status': 'published',
                'display_order': 6,
                'show_in_footer': True,
                'seo_title': 'Shipping Information — Delivery Details',
                'seo_description': 'Everything you need to know about our delivery options, timeframes, and charges.',
                'content': """<h2>Shipping Information</h2>

<h3>Delivery Timeframes</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse; width:100%;">
  <thead style="background:#f0f0f0;">
    <tr><th>Location</th><th>Standard</th><th>Express</th></tr>
  </thead>
  <tbody>
    <tr><td>Karachi, Lahore, Islamabad</td><td>2-3 Days</td><td>Next Day</td></tr>
    <tr><td>Faisalabad, Multan, Peshawar</td><td>3-4 Days</td><td>1-2 Days</td></tr>
    <tr><td>Other Cities</td><td>4-6 Days</td><td>2-3 Days</td></tr>
    <tr><td>Remote Areas</td><td>6-10 Days</td><td>Not Available</td></tr>
  </tbody>
</table>

<h3>Shipping Charges</h3>
<ul>
  <li>Standard Delivery: Rs. 200</li>
  <li>Express Delivery: Rs. 400</li>
  <li>Free Delivery on orders over Rs. 5,000</li>
</ul>

<h3>Order Tracking</h3>
<p>After dispatch, you'll receive an SMS with your tracking number. Track your order anytime on our tracking page or by calling customer support.</p>"""
            },
        ]

        for data in pages:
            Page.objects.create(store=store, **data)

        self.stdout.write(f'   📄  Added {len(pages)} static pages.')

    def _seed_homepage_sections(self, store):
        if HomepageSection.objects.filter(store=store).exists():
            self.stdout.write('   ⏭  Homepage sections already exist, skipping.')
            return

        defaults = [
            ('slider', 'Hero Banner Slider', '', 10),
            ('categories', 'Featured Categories', 'Explore our top category lines', 20),
            ('featured_products', 'Featured Products', 'Premium items selected for you', 30),
            ('new_arrivals', 'New Arrivals', 'Fresh stock just landed', 40),
            ('top_selling', 'Best Sellers', 'Most popular products this week', 50),
            ('sale_products', 'Flash Sale Items', 'Limited time discounts — grab them fast!', 60),
            ('middle_banners', 'Promotional Banners', '', 70),
            ('reviews', 'Customer Reviews', 'Hear what our happy customers say', 80),
        ]
        for key, title, subtitle, order in defaults:
            HomepageSection.objects.create(
                store=store, section_key=key, title=title,
                subtitle=subtitle, display_order=order, is_active=True
            )
        self.stdout.write(f'   🏠  Added {len(defaults)} homepage sections.')

    def _seed_site_settings(self, store):
        obj, created = SiteSettings.objects.get_or_create(store=store)
        if created or not obj.announcement_bar_text:
            obj.announcement_bar_enabled = True
            obj.announcement_bar_text = '🚚 FREE Delivery on orders over Rs. 5,000 | Use code WELCOME10 for 10% off first order!'
            obj.announcement_bar_color = '#0f172a'
            obj.footer_description = f'{store.name} brings you the best products at unbeatable prices. Fast delivery, easy returns, and dedicated customer support.'
            obj.copyright_text = f'© 2025 {store.name}. All rights reserved.'
            obj.free_shipping_threshold = 5000
            obj.default_shipping_charge = 200
            obj.sticky_header = True
            obj.search_enabled = True
            obj.wishlist_enabled = True
            obj.cart_enabled = True
            obj.cod_enabled = True
            obj.seo_title = f'{store.name} — Online Shopping Pakistan'
            obj.seo_description = f'Shop at {store.name} for the best deals on electronics, fashion, and more. Fast delivery across Pakistan.'
            obj.save()
            self.stdout.write('   ⚙️  Site settings seeded.')
        else:
            self.stdout.write('   ⏭  Site settings already configured, skipping.')
