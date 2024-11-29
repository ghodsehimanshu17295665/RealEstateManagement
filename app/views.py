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
from .models import User, Profile, Category, Property, Booking
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator


# Home Page -
class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


# Signup view :-
class SignUpView(View):
    template_name = "registration/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect(reverse_lazy("login_page"))
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
            if user:
                login(request, user)
                # Redirect based on role
                if user.role == "SELLER":
                    return redirect("home_page")
                else:
                    return redirect("home_page")
        messages.error(request, "Invalid username or password. Please try again.")
        return render(request, "registration/login.html", {"form": form})


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
        page_number = request.GET.get('page', 1)  # Get the page number from query parameters
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


# Buyer related views :-
# Show all Property in Buyer Dashboard..,
class AllPropertyView(ListView):
    model = Property
    template_name = 'buyer/all_property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.all().order_by('-id')


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
        return render(request, "buyer/buyer_profile_update.html", {"form": form})

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


class AddBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, id=pk)

        # Prevent duplicate bookings
        existing_booking = Booking.objects.filter(property=property_obj, buyer=request.user).exists()
        if existing_booking:
            # Handle duplicate booking case
            return redirect('booking_list')

        Booking.objects.create(property=property_obj, buyer=request.user)
        return redirect('booking_list')


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "buyer/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(buyer=self.request.user).select_related('property')
