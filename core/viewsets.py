from rest_framework import viewsets
from .permissions import IsStoreStaff


class TenantScopedModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset for every store-scoped resource (Product, Stock, Order...).
    Automatically filters querysets to request.store and stamps request.store
    onto every object created through it. Subclasses just set `queryset` and
    `serializer_class` — never filter by store manually, it happens here once.
    """
    permission_classes = [IsStoreStaff]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_platform_admin and not self.request.store:
            return qs
        return qs.filter(store=self.request.store)

    def perform_create(self, serializer):
        serializer.save(store=self.request.store)