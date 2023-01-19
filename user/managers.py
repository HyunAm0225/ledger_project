from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        extra_fields["username"] = email
        extra_fields["created_at"] = timezone.now()
        extra_fields["updated_at"] = timezone.now()
        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )

        if password:
            user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def customers(self):
        return self.get_queryset().filter(Q(is_staff=False) | (Q(is_staff=True)))

    def staff(self):
        return self.get_queryset().filter(is_staff=True)
