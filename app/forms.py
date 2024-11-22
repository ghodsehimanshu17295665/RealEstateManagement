from django import forms

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Property, Category, Booking, Profile


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        }


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
    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'gender']  # Add your fields here

    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    profile_picture = forms.ImageField(required=False)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


# Profile forms for Buyer and Seller
class SellerForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "user",
            "birth_date",
            "gender",
        )


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ("title", "description", "price", "location", "status", "image", "seller", "category")


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('property', 'buyer', 'status')
