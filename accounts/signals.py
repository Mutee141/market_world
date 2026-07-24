from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up, user_logged_in
from tenants.models import Store
from customers.models import Customer

User = get_user_model()


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    """
    Triggered when a user completes sign-up via Allauth (including Google OAuth).
    Ensures role is CUSTOMER and creates linked Customer profile for current store.
    """
    if user.role not in [User.Role.SUPER_ADMIN, User.Role.OWNER, User.Role.MANAGER]:
        user.role = User.Role.CUSTOMER
        user.save(update_fields=['role'])

    store = getattr(request, 'store', None) if request else None
    if not store:
        store = Store.objects.filter(is_active=True).first()

    if store and not Customer.objects.filter(user=user).exists():
        full_name = user.get_full_name() or user.first_name or user.username or "Google Customer"
        Customer.objects.create(
            store=store,
            user=user,
            full_name=full_name,
            email=user.email or '',
            phone=getattr(user, 'phone', '') or ''
        )


@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    """
    Guarantees Customer profile exists on social/regular login for customer-level users.
    """
    if user.role == User.Role.CUSTOMER or not user.role:
        store = getattr(request, 'store', None) if request else None
        if not store:
            store = Store.objects.filter(is_active=True).first()

        if store and not Customer.objects.filter(user=user).exists():
            full_name = user.get_full_name() or user.first_name or user.username or "Store Customer"
            Customer.objects.create(
                store=store,
                user=user,
                full_name=full_name,
                email=user.email or '',
                phone=getattr(user, 'phone', '') or ''
            )
