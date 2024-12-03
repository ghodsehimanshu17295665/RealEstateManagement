from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import (
    ListView,
    TemplateView,
    View,
    CreateView,
    DetailView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignUpForm,
    ProfileUpdateForm,
    PropertyForm,
)
from .models import User, Profile, Category, Property, Booking
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView
from .email_utils import send_verification_email


# Home Page -
class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


# Signup view :-
class SignUpView(View):
    template_name = "registration/signup.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        # form = SignUpForm(request.POST)
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user, request)
            messages.success(
                request, "Account created successfully! You are now logged in."
            )
            return redirect("login_page")
        return render(request, "registration/signup.html", {"form": form})


# Login View Function
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                # Check if the user's email is verified
                if not user.email_verified:
                    # Token handling logic here
                    if user.is_token_valid():
                        user.generate_verification_token()
                        send_verification_email(user, request)
                        messages.error(
                            request,
                            "Your email is not verified. A new verification link has been sent to your email.",
                        )
                        return redirect("login")
                else:
                    login(request, user)
                    messages.success(request, "Logged in successfully!")
                    return self.redirect_based_on_role(user)
            else:
                messages.error(
                    request, "Invalid username or password. Please try again."
                )
        return render(request, "registration/login.html", {"form": form})

    def redirect_based_on_role(self, user):
        if user.role == "SELLER":
            return redirect("home_page")
        return redirect("home_page")


# Activate Account View :-
class ActivateAccountView(View):
    def get(self, request, uid, token):
        user = User.objects.filter(id=uid, verification_token=token).first()

        if user and user.is_token_valid():
            user.email_verified = True
            user.verification_token = None
            user.token_created_at = None
            user.save()
            messages.success(
                request,
                "Thank you for verifying your email. You can now log in.",
            )
            return redirect("login_page")
        elif user:
            user.generate_verification_token()
            send_verification_email(user, request)
            messages.error(
                request,
                "Your email verification link has expired. A new verification link has been sent to your email.",
            )
            return redirect("login_page")
        else:
            messages.error(request, "Invalid verification link.")
            return redirect("login_page")


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
        return render(request, "seller/view_listing.html")


# Seller Profile :-
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_page")

        data = Profile.objects.filter(user=request.user).first()
        context = {"data": data}
        return render(request, "seller/seller_profile.html", context)


# Update seller Profile Views:-
class UpdateProfileView(View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(instance=profile, user=request.user)
        return render(
            request, "seller/seller_profile_update.html", {"form": form}
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
            request, "seller/seller_profile_update.html", {"form": form}
        )


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

        # Set up pagination (2 items per page)
        paginator = Paginator(properties, 2)  # Show 2 properties per page
        page_number = request.GET.get(
            "page", 1
        )  # Get the page number from query parameters
        page_obj = paginator.get_page(page_number)  # Get the specific page

        # Pass the page_obj to the template
        return render(request, self.template_name, {"page_obj": page_obj})


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


# Remove Property Views :-
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


# change Passwoard for Seller :-
class ChangePasswoardSellerView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("buyer_dashboard")
    template_name = "seller/change_password.html"


# Buyer related views :-
# Show all Property in Buyer Dashboard..,
class AllPropertyView(ListView):
    model = Property
    template_name = "buyer/all_property_list.html"
    context_object_name = "properties"

    def get_queryset(self):
        return Property.objects.all().order_by("-id")


# Buyer Profile View :-
class BuyerProfile(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login_page")

        profile, created = Profile.objects.get_or_create(user=request.user)
        context = {"data": profile}
        return render(request, "buyer/buyer_profile.html", context)


# Buyer Profile Update View :-
class UpdateBuyerProfile(View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(instance=profile, user=request.user)
        return render(
            request, "buyer/buyer_profile_update.html", {"form": form}
        )

    def post(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile, user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("buyer_profile")
        return render(
            request, "buyer/buyer_profile_update.html", {"form": form}
        )


# Property Add for booking list :-
class AddBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, id=pk)

        # Prevent duplicate bookings
        existing_booking = Booking.objects.filter(
            property=property_obj, buyer=request.user
        ).exists()
        if existing_booking:
            # Handle duplicate booking case
            return redirect("booking_list")

        Booking.objects.create(property=property_obj, buyer=request.user)
        return redirect("booking_list")


# Book Property list :-
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "buyer/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(buyer=self.request.user).select_related(
            "property"
        )


# Property detail View :-
class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = "buyer/property_detail.html"
    context_object_name = "property"


# # Remove Property for Booking List :-
class RemoveBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, id=pk, buyer=request.user)
        booking.delete()
        return redirect("booking_list")


# change Passwoard for buyer :-
class ChangePasswoardBuyerView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("buyer_dashboard")
    template_name = "buyer/change_password.html"
