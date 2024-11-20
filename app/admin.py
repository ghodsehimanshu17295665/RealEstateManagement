from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

from .models import User, Category, Property, Booking, Transaction, Payment, Profile


@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "id",
        "username",
        "email",
        "role",
        "phone_number",
        "address",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "created_at")
    search_fields = ("username", "email", "phone_number", "role")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "role",
                    "phone_number",
                    "address",
                    # "email_verified",
                    # "verification_token",
                    # "token_created_at",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "phone_number",
                    "address",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "birth_date", "gender")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'status', 'location', 'seller', 'category', 'image')


@admin.register(Booking)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'buyer', 'booking_date', 'status')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'buyer', 'transaction_type', 'amount')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'amount_paid', 'payment_method', 'status')
