from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    Home,
    SignUpView,
    LoginView,
    LogoutView,
    BuyerDashboardView,
    SellerDashboardView,
    ProfileView,
    UpdateProfileView,
    PropertyList_View,
    CreatePropertyView,
    UpdatePropertyView,
    DeletePropertyView,
    AllPropertyView,
    BuyerProfile,
    UpdateBuyerProfile,
    AddBookingView,
    BookingListView,
    PropertyDetailView,
    RemoveBookingView,
    ChangePasswoardSellerView,
    ChangePasswoardBuyerView,
    ActivateAccountView,
)

urlpatterns = [
    # Home Page
    path("", Home.as_view(), name="home_page"),
    path("signup/", SignUpView.as_view(), name="signup_page"),
    path("login/", LoginView.as_view(), name="login_page"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # email verification
    path(
        "activate/<uuid:uid>/<str:token>/",  # <uuid:uid> for UUID type
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path(
        "buyer-dashboard/",
        BuyerDashboardView.as_view(),
        name="buyer_dashboard",
    ),
    path(
        "seller-dashboard/",
        SellerDashboardView.as_view(),
        name="seller_dashboard",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "profile/update/", UpdateProfileView.as_view(), name="update_profile"
    ),
    path("list/property/", PropertyList_View.as_view(), name="property_list"),
    path(
        "create/property/",
        CreatePropertyView.as_view(),
        name="create_property",
    ),
    path(
        "property/update/<uuid:pk>/",
        UpdatePropertyView.as_view(),
        name="update_property",
    ),
    path(
        "property/delete/<uuid:pk>/",
        DeletePropertyView.as_view(),
        name="delete_property",
    ),
    path("all-properties/", AllPropertyView.as_view(), name="all_properties"),
    path("buyer/profile/", BuyerProfile.as_view(), name="buyer_profile"),
    path(
        "buyer/profile/update/",
        UpdateBuyerProfile.as_view(),
        name="update_buyer_profile",
    ),
    path(
        "properties/<uuid:pk>/add-booking/",
        AddBookingView.as_view(),
        name="add_booking",
    ),
    path("my-bookings/", BookingListView.as_view(), name="booking_list"),
    path(
        "property/<uuid:pk>/",
        PropertyDetailView.as_view(),
        name="property_details",
    ),
    path(
        "remove-booking/<uuid:pk>/",
        RemoveBookingView.as_view(),
        name="remove_booking",
    ),
    path(
        "change-password/",
        ChangePasswoardBuyerView.as_view(),
        name="change_password_buyer",
    ),
    path(
        "change-password/",
        ChangePasswoardSellerView.as_view(),
        name="change_password_seller",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
