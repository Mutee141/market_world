import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Ensures active Super Admin accounts exist for website dashboard access"

    def handle(self, *args, **options):
        # Admin accounts to guarantee exist with requested credentials
        accounts = [
            {
                "username": os.environ.get("ADMIN_USERNAME", "market"),
                "email": "market@marketworld.com",
                "password": os.environ.get("ADMIN_PASSWORD", "123")
            },
            {
                "username": "admin",
                "email": "admin@marketworld.com",
                "password": "123"
            }
        ]

        for acc in accounts:
            username = acc["username"]
            email = acc["email"]
            password = acc["password"]

            user = User.objects.filter(username__iexact=username).first()
            if not user:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                user.role = getattr(User.Role, 'SUPER_ADMIN', 'SUPER_ADMIN')
                user.save()
                self.stdout.write(self.style.SUCCESS(f"[SUCCESS] Created superadmin account: '{username}' with password: '{password}'"))
            else:
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                user.role = getattr(User.Role, 'SUPER_ADMIN', 'SUPER_ADMIN')
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"[SUCCESS] Configured superadmin '{username}' with password '{password}'"))
