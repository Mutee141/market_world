from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, StorePublicDetailView, MyStoreSettingsView

router = DefaultRouter()
router.register('stores', StoreViewSet, basename='stores')

urlpatterns = [
    path('public/store/', StorePublicDetailView.as_view(), name='store-public'),
    path('my-store/', MyStoreSettingsView.as_view(), name='my-store-settings'),
    path('', include(router.urls)),
]