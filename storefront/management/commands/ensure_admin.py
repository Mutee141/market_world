import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Ensures an active Super Admin exists for website dashboard access"

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@marketworld.com")
        password = os.environ.get("ADMIN_PASSWORD", "Admin123456!")

        admin_user = User.objects.filter(username=username).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            admin_user.role = getattr(User.Role, 'SUPER_ADMIN', 'SUPER_ADMIN')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"[SUCCESS] Created superadmin account: '{username}' with password: '{password}'"))
        else:
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.role = getattr(User.Role, 'SUPER_ADMIN', 'SUPER_ADMIN')
            admin_user.set_password(password)
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"[SUCCESS] Updated existing superadmin '{username}' credentials"))
