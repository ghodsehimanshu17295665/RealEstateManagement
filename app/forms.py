from django import forms

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Property, Category, Booking, Profile


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "password1",
            "password2",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Confirm your password",
                }
            ),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.username = None  # Explicitly set username to None or ignore
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("user", "birth_date", "gender")


class ProfileUpdateForm(forms.ModelForm):
    # Fields from the User model
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    phone_number = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ["birth_date", "gender"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            # Pre-fill User fields
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["profile_picture"].initial = user.profile_picture
            self.fields["phone_number"].initial = user.phone_number
            self.fields["address"].initial = user.address

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user

        # Save User fields
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.address = self.cleaned_data["address"]

        if commit:
            user.save()
            profile.save()

        return profile


# Profile forms for Buyer and Seller
class SellerForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "user",
            "birth_date",
            "gender",
        )


# Property Form
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            "title",
            "description",
            "price",
            "location",
            "status",
            "image",
            "category",
        )  # Removed 'seller'
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter description",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Enter price",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter location",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("property", "buyer", "status")
