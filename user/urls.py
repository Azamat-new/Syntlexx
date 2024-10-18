from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/bookings/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('api/user/bookings/<int:booking_id>/', views.UserBookingsView.as_view(), name='cancel-booking'),
    path('profile/tours/create/', views.UserTourCreationView.as_view(), name='create-tour'),
    path('profile/tours/<int:tour_id>/edit/', views.UserTourCreationView.as_view(), name='edit-tour'),
    path('profile/withdraw/', views.UserWithdrawFundsView.as_view(), name='withdraw-funds'),
]