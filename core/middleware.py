from django.utils.deprecation import MiddlewareMixin
from tenants.models import Store


class TenantMiddleware(MiddlewareMixin):
    """
    Resolves which Store (tenant) the current request belongs to and attaches
    it to request.store. Resolution order:
      1. Custom domain match
      2. Subdomain match (hbk.yourplatform.com -> slug 'hbk')
      3. X-Store-Slug header (local dev / mobile apps)
      4. ?store=slug query param (handy for browser testing)
    request.store is None for platform-level routes (super admin, auth, etc.)
    """

    PLATFORM_SUBDOMAINS = {'www', 'api', 'admin', 'app', 'localhost', '127.0.0.1'}

    def process_request(self, request):
        request.store = Store.objects.filter(is_active=True).first()