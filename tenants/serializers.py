from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    """Full detail — platform super admin manages any store with this."""
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['slug', 'status']


class StorePublicSerializer(serializers.ModelSerializer):
    """Public-safe subset for the storefront — no owner/plan/status exposed to shoppers."""
    class Meta:
        model = Store
        fields = ['id', 'name', 'slug', 'logo', 'banner', 'primary_color',
                  'phone', 'email', 'address', 'city', 'currency']


class StoreSettingsSerializer(serializers.ModelSerializer):
    """Store Owner edits their OWN branding/settings — plan/status stay platform-controlled."""
    class Meta:
        model = Store
        fields = ['name', 'logo', 'banner', 'primary_color', 'phone',
                  'email', 'address', 'city', 'tax_percentage']