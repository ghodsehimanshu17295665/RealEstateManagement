from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

    def create_buyer(self, email, password=None, **extra_fields):
        """
        Create and return a buyer user.
        """
        extra_fields.setdefault('role', 'buyer')
        return self.create_user(email, password, **extra_fields)

    def create_seller(self, email, password, **extra_fields):
        """
        Create and return a seller user.
        """
        extra_fields.setdefault('role', 'seller')
        return self.create_user(email, password, **extra_fields)
