from django import forms

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Property, Category, Booking, Profile


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "password1", "password2"]


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


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ("title", "description", "price", "location", "status", "image", "seller", "category")


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('property', 'buyer', 'status')
