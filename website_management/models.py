import os
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import TenantModel, TimeStampedModel


def hero_slide_upload_to(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    title_slug = slugify(getattr(instance, 'title', 'hero-slide')) or 'hero-slide'
    return os.path.join('hero_slides', f"{title_slug}.{ext}")


def hero_slide_mobile_upload_to(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    title_slug = slugify(getattr(instance, 'title', 'hero-slide')) or 'hero-slide'
    return os.path.join('hero_slides', 'mobile', f"{title_slug}-mobile.{ext}")


def banner_upload_to(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    title_slug = slugify(getattr(instance, 'title', 'banner')) or 'banner'
    return os.path.join('banners', f"{title_slug}.{ext}")


def banner_mobile_upload_to(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    title_slug = slugify(getattr(instance, 'title', 'banner')) or 'banner'
    return os.path.join('banners', 'mobile', f"{title_slug}-mobile.{ext}")


def media_library_upload_to(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    title_slug = slugify(getattr(instance, 'title', filename.split('.')[0])) or 'media'
    return os.path.join('media_library', f"{title_slug}.{ext}")


class SiteSettings(models.Model):
    """
    One-row settings table per store.
    Controls store-wide appearance, SEO defaults, announcements and social links.
    """
    store = models.OneToOneField(
        'tenants.Store', on_delete=models.CASCADE, related_name='site_settings'
    )

    # Branding
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    logo_text = models.CharField(max_length=80, blank=True)

    # Announcement bar
    announcement_bar_text = models.CharField(max_length=255, blank=True)
    announcement_bar_enabled = models.BooleanField(default=False)
    announcement_bar_color = models.CharField(max_length=7, default='#0F172A')

    # SEO defaults
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.TextField(blank=True)

    # Social media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    # Shipping & Charges
    free_shipping_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    default_shipping_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Operational
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, default='We are currently under maintenance. Please check back later.')

    # Footer
    footer_description = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=255, blank=True)

    # Feature Strip (footer top bar — 4 configurable items)
    feature_1_title = models.CharField(max_length=80, blank=True, default='Free Shipping')
    feature_1_text = models.CharField(max_length=120, blank=True, default='On orders over $50')
    feature_2_title = models.CharField(max_length=80, blank=True, default='24/7 Support')
    feature_2_text = models.CharField(max_length=120, blank=True, default='Always here to help')
    feature_3_title = models.CharField(max_length=80, blank=True, default='Secure Payments')
    feature_3_text = models.CharField(max_length=120, blank=True, default='100% protected')
    feature_4_title = models.CharField(max_length=80, blank=True, default='Easy Returns')
    feature_4_text = models.CharField(max_length=120, blank=True, default='30-day policy')

    # Layout Options (Header/Footer management)
    sticky_header = models.BooleanField(default=True)
    search_enabled = models.BooleanField(default=True)
    wishlist_enabled = models.BooleanField(default=True)
    cart_enabled = models.BooleanField(default=True)

    # Business Options (Payment)
    cod_enabled = models.BooleanField(default=True)
    bank_transfer_enabled = models.BooleanField(default=False)

    # SMTP Configurations
    smtp_host = models.CharField(max_length=255, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=255, blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f"Settings for {self.store.name}"


class HeroSlide(TenantModel):
    """Hero banner slider shown at the top of the homepage."""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    badge = models.CharField(max_length=100, blank=True, help_text="e.g. 'HOT DEAL' or 'NEW ARRIVAL'")
    image = models.ImageField(upload_to=hero_slide_upload_to)
    mobile_image = models.ImageField(upload_to=hero_slide_mobile_upload_to, blank=True, null=True)
    button_text = models.CharField(max_length=60, blank=True)
    button_link = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    # Styles and alignments
    overlay_enabled = models.BooleanField(default=True)
    text_alignment = models.CharField(
        max_length=10,
        choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')],
        default='left'
    )
    text_color = models.CharField(max_length=20, default='#000000', help_text="CSS Color code e.g. '#ffffff' or 'white'")
    animation_type = models.CharField(max_length=50, blank=True, default='fade')
    countdown_end = models.DateTimeField(null=True, blank=True, help_text="Optional event countdown timer end date")
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class PromotionalBanner(TenantModel):
    """
    Banners shown in different page positions:
    home_top, home_middle, home_bottom, category_page, product_page, sidebar, footer
    """
    POSITION_CHOICES = (
        ('home_top', 'Home — Top'),
        ('home_middle', 'Home — Middle'),
        ('home_bottom', 'Home — Bottom'),
        ('category_page', 'Category Page'),
        ('product_page', 'Product Page'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
    )

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=banner_upload_to)
    mobile_image = models.ImageField(upload_to=banner_mobile_upload_to, blank=True, null=True)
    button_text = models.CharField(max_length=60, blank=True)
    button_link = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, default='home_top')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Design and Scheduling
    background_color = models.CharField(max_length=20, default='#ffffff', help_text="e.g. '#f8f9fa' or 'black'")
    text_color = models.CharField(max_length=20, default='#000000')
    alt_text = models.CharField(max_length=200, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['position', 'display_order']

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"

    @property
    def is_live(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class Page(TenantModel):
    """
    CMS static pages: About Us, Privacy Policy, Terms, FAQ, etc.
    Managed from the admin dashboard.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    content = models.TextField(blank=True)
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    # CMS Extended fields
    hero_image = models.ImageField(upload_to='pages/hero/', blank=True, null=True)
    featured_image = models.ImageField(upload_to='pages/featured/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    publish_date = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'slug')
        ordering = ['display_order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        if not self.is_active:
            return False
        if self.status == 'draft':
            return False
        if self.status == 'scheduled' and timezone.now() < self.publish_date:
            return False
        return True


class MenuItem(TenantModel):
    """Navigation menu items for the storefront header/footer/sidebar."""
    MENU_LOCATION_CHOICES = (
        ('header', 'Header Navigation'),
        ('footer', 'Footer Navigation'),
        ('mega_menu', 'Mega Menu'),
    )

    label = models.CharField(max_length=80)
    url = models.CharField(max_length=255, blank=True, help_text="Custom URL, or leave blank if using category")
    category = models.ForeignKey(
        'catalog.Category', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='menu_items'
    )
    location = models.CharField(max_length=20, choices=MENU_LOCATION_CHOICES, default='header')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    # Advanced navigation nesting
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class name (e.g. 'fa-laptop')")

    class Meta:
        ordering = ['location', 'display_order']

    def __str__(self):
        return f"{self.label} [{self.get_location_display()}]"

    @property
    def resolved_url(self):
        if self.category:
            return f"/shop/?category={self.category.slug}"
        return self.url or '#'


class HomepageSection(TenantModel):
    """Configure homepage dynamic components display state and order."""
    SECTION_CHOICES = (
        ('slider', 'Hero Banner Slider'),
        ('categories', 'Featured Categories'),
        ('featured_products', 'Featured Products Grid'),
        ('new_arrivals', 'New Arrivals Grid'),
        ('top_selling', 'Top Selling Grid'),
        ('sale_products', 'Discounted Items Grid'),
        ('middle_banners', 'Promotional Banners Row'),
        ('reviews', 'Customer Testimonials'),
        ('special_offers', 'Special Offers'),
        ('recently_added', 'Recently Added'),
        ('flash_sale', 'Flash Sale'),
        ('trending_products', 'Trending Products'),
        ('deal_of_the_day', 'Deal of the Day'),
        ('why_choose_us', 'Why Choose Us'),
        ('brands', 'Brands'),
        ('newsletter', 'Newsletter'),
    )

    section_key = models.CharField(max_length=50, choices=SECTION_CHOICES)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    products = models.ManyToManyField('catalog.Product', blank=True, related_name='homepage_sections')

    class Meta:
        ordering = ['display_order']
        unique_together = ('store', 'section_key')

    def __str__(self):
        return f"{self.get_section_key_display()} ({self.title})"


class MediaFile(TenantModel):
    """Centralized media library for uploading images and files once and reusing them."""
    file = models.ImageField(upload_to=media_library_upload_to)
    title = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or self.file.name


class ContactMessage(TenantModel):
    """
    Stores contact form submissions from the storefront.
    Visible in the admin dashboard under 'Contact Messages'.
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"From {self.name} — {self.subject or 'No Subject'}"
