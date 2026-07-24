from rest_framework.permissions import BasePermission


class IsPlatformAdmin(BasePermission):
    """Only the SaaS platform's own super admins — manages all stores."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_platform_admin)


class IsStoreStaff(BasePermission):
    """
    Base permission for every store-scoped API. Requires:
      - a resolved store (via TenantMiddleware, from subdomain/header/query param)
      - the logged-in user belongs to THAT exact store (or is a platform admin)
    This is what physically prevents Store A's staff from ever touching
    Store B's data, even if they guess an object ID.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_platform_admin:
            return True
        if not request.store:
            return False
        return request.user.store_id == request.store.id


class IsOwnerOrManager(IsStoreStaff):
    """Tenant scoping PLUS a role restriction — for sensitive actions
    (editing products, deleting stock, managing staff, seeing cost prices)."""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_platform_admin:
            return True
        return request.user.role in ('owner', 'manager')