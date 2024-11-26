from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import (
    ListView,
    TemplateView,
    View,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignUpForm,
    ProfileUpdateForm,
    PropertyForm,
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
                    request,
                    "Account created successfully! You are now logged in.",
                )
                return redirect(reverse_lazy("login_page"))
            else:
                messages.error(
                    request, "Authentication failed. Please try again."
                )
        else:
            messages.error(
                request,
                "There was an error with your submission. Please try again.",
            )

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
                return redirect("home_page")
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
        return render(request, "buyer/buyer_dashboard.html")


class SellerDashboardView(LoginRequiredMixin, View):
    """Seller Dashboard View"""

    def get(self, request):
        return render(request, "seller/seller_dashboard.html")


# Profile myProfile :-
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_page")

        data = Profile.objects.filter(user=request.user).first()
        context = {"data": data}
        return render(request, "registration/profile.html", context)


# Update User Profile Views:-
class UpdateProfileView(View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(instance=profile, user=request.user)
        return render(
            request, "registration/update_profile.html", {"form": form}
        )

    def post(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile, user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(
            request, "registration/update_profile.html", {"form": form}
        )


# Listing views :-
class Listing_View(LoginRequiredMixin, ListView):
    model = Property
    template_name = "seller/view_listing.html"
    context_object_name = "properties"

    def get_queryset(self):
        return Property.objects.filter(seller=self.request.user)


# Create Property Views :-
class CreatePropertyView(View):
    template_name = "seller/create_property.html"

    def get(self, request):
        form = PropertyForm()
        categories = Category.objects.all()
        return render(
            request,
            self.template_name,
            {"form": form, "categories": categories},
        )

    def post(self, request):
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.seller = request.user
            property_instance.save()
            messages.success(
                request, "Your property has been created successfully!"
            )
            return redirect("property_list")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {"form": form})


# Property List Views :-
class PropertyList_View(TemplateView):
    template_name = "seller/list_property.html"

    def get(self, request):
        properties = Property.objects.filter(seller=request.user)
        return render(request, self.template_name, {"properties": properties})


# Update Property Views :-
class UpdatePropertyView(View):
    template_name = "seller/update_property.html"

    def get(self, request, pk):
        property_instance = get_object_or_404(
            Property, pk=pk, seller=request.user
        )
        form = PropertyForm(instance=property_instance)
        categories = Category.objects.all()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "categories": categories,
                "property": property_instance,
            },
        )

    def post(self, request, pk):
        property_instance = get_object_or_404(
            Property, pk=pk, seller=request.user
        )
        form = PropertyForm(
            request.POST, request.FILES, instance=property_instance
        )
        categories = Category.objects.all()

        if form.is_valid():
            form.save()
            messages.success(
                request, "Your Property has been updated successfully!"
            )
            return redirect("property_list")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "categories": categories,
                "property": property_instance,
            },
        )


class DeletePropertyView(View):
    template_name = "seller/delete_property.html"

    def get(self, request, pk):
        property_instance = get_object_or_404(
            Property, pk=pk, seller=request.user
        )
        return render(
            request, self.template_name, {"property": property_instance}
        )

    def post(self, request, pk):
        property_instance = get_object_or_404(
            Property, pk=pk, seller=request.user
        )
        property_instance.delete()
        messages.success(request, "Property has been deleted successfully.")
        return redirect("property_list")
