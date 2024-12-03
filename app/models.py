import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from .managers import CustomUserManager


class TimeStampeModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class User(TimeStampeModel, AbstractUser):
    username = None
    ROLE_CHOICES = [
        ("BUYER", "Buyer"),
        ("SELLER", "Seller"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="BUYER"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        default="profile_pics/default_profile_pic.jpg",
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_verification_token(self):
        self.verification_token = str(uuid.uuid4())
        self.token_created_at = timezone.now()
        self.save()

    def is_token_valid(self):
        if self.token_created_at:
            return (
                timezone.now() - self.token_created_at
            ) < timezone.timedelta(hours=24)
        return False


class Profile(TimeStampeModel):
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


class Category(TimeStampeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Property(TimeStampeModel):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("SOLD", "Sold"),
        ("RENTED", "Rented"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="AVAILABLE"
    )
    image = models.ImageField(upload_to="properties/", null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="properties"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_products"
    )

    def __str__(self):
        return self.title


# Booking Model
class Booking(TimeStampeModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="bookings"
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING"
    )

    def __str__(self):
        return f"Booking for {self.property.title} by {self.buyer.username}"


# Transaction Model
class Transaction(TimeStampeModel):
    TRANSACTION_TYPE_CHOICES = [
        ("SALE", "Sale"),
        ("RENTAL", "Rental"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="transactions"
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPE_CHOICES
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"Transaction for {self.property.title} by {self.buyer.username}"
        )


# Payment Model
class Payment(TimeStampeModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="payments"
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING"
    )

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.transaction.property.title if self.transaction else 'Unknown Property'}"
