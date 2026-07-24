from django.contrib import admin
from .models import SiteSettings, HeroSlide, PromotionalBanner, Page, MenuItem


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('store', 'announcement_bar_enabled', 'maintenance_mode')


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'display_order', 'is_active')
    list_filter = ('is_active',)


@admin.register(PromotionalBanner)
class PromotionalBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'position', 'display_order', 'is_active')
    list_filter = ('position', 'is_active')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'slug', 'is_active', 'show_in_footer')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'store', 'location', 'display_order', 'is_active')
    list_filter = ('location', 'is_active')
