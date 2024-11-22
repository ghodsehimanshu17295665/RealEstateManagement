from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, ListView, TemplateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignUpForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProfileUpdateForm
)
from .models import User, Profile, Category, Property
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm


class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


class SignUpView(View):
    template_name = "registration/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            if user:
                # Create a profile for the user
                Profile.objects.create(
                    user=user,
                    birth_date=None,
                    gender=None,
                )
                # Log the user in
                login(request, user)

                messages.success(
                    request, "Account created successfully! You are now logged in."
                )
                return redirect(reverse_lazy("login_page"))
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "There was an error with your submission. Please try again.")

        return render(request, self.template_name, {"form": form})


# Login View Function
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_page')
        return render(request, "registration/login.html", {"form": form})


class HouseView(TemplateView):
    template_name = "registration/login.html"


# Logout
class LogoutView(View):
    template_name = "registration/logout.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect("/")


class BuyerDashboardView(LoginRequiredMixin, View):
    """Buyer Dashboard View"""

    def get(self, request):
        return render(request, 'buyer/buyer_dashboard.html')


class SellerDashboardView(LoginRequiredMixin, View):
    """Seller Dashboard View"""

    def get(self, request):
        return render(request, 'seller/seller_dashboard.html')


# Profile myProfile :-
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_page")

        data = Profile.objects.filter(user=request.user).first()
        context = {"data": data}
        return render(request, "registration/profile.html", context)


# class UpdateProfileView(View):
#     def get(self, request):
#         # Get the profile for the logged-in user
#         profile = Profile.objects.filter(user=request.user).first()

#         # Populate the form with the existing profile data
#         form = ProfileForm(instance=profile)
#         return render(request, 'registration/update_profile.html', {'form': form})

#     def post(self, request):
#         # Get the profile for the logged-in user
#         profile = Profile.objects.get(user=request.user)

#         # Populate the form with updated data
#         form = ProfileForm(request.POST, request.FILES, instance=profile)

#         if form.is_valid():
#             form.save()  # Save the updated profile
#             return redirect('profile')  # Redirect back to the profile page

#         return render(request, 'registration/update_profile.html', {'form': form})


class UpdateProfileView(View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(instance=profile)
        return render(request, "registration/update_profile.html", {"form": form})

    def post(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_page")  # Redirect to the profile page after update
        return render(request, "registration/update_profile.html", {"form": form})

# class UpdateProfileView(LoginRequiredMixin, TemplateView):
#     template_name = "registration/updateprofile.html"
#     login_url = "/login/"  # Redirect URL for unauthorized users

#     def get(self, request):
#         profile = Profile.objects.filter(user=request.user).first()
#         form = ProfileUpdateForm(
#             instance=profile, initial={"first_name": request.user.first_name}
#         )
#         return render(request, self.template_name, {"form": form})

#     def post(self, request):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, "Your profile has been updated successfully!"
#             )
#             return redirect("profile_page")
#         else:
#             messages.error(request, "Please correct the errors below.")

#         return render(request, self.template_name, {"form": form})