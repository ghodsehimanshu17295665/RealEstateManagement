from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Home, SignUpView, LoginView, HouseView, LogoutView, BuyerDashboardView, SellerDashboardView, ProfileView, UpdateProfileView

urlpatterns = [
    # Home Page
    path("", Home.as_view(), name="home_page"),
    path("signup/", SignUpView.as_view(), name="signup_page"),
    path("login/", LoginView.as_view(), name="login_page"),
    path("house/", HouseView.as_view(), name="house_page"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('buyer-dashboard/', BuyerDashboardView.as_view(), name='buyer_dashboard'),
    path('seller-dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
