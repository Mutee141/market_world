from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from core.permissions import IsPlatformAdmin, IsOwnerOrManager
from .models import Store
from .serializers import (
    StoreSerializer, StorePublicSerializer, StoreSettingsSerializer
)


class StoreViewSet(viewsets.ModelViewSet):
    """Platform admin only — onboard/suspend/manage every store on the platform."""
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsPlatformAdmin]


class StorePublicDetailView(generics.RetrieveAPIView):
    """Public, no auth — storefront fetches branding based on the resolved subdomain."""
    serializer_class = StorePublicSerializer
    permission_classes = []
    authentication_classes = []

    def get_object(self):
        if not self.request.store:
            raise NotFound("No store resolved for this domain.")
        return self.request.store


class MyStoreSettingsView(generics.RetrieveUpdateAPIView):
    """Owner/Manager edits their OWN store's settings only."""
    serializer_class = StoreSettingsSerializer
    permission_classes = [IsOwnerOrManager]

    def get_object(self):
        return self.request.store