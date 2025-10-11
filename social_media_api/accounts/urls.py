from django.urls import path,include
from .views import UserRegistrationView, UserLoginView, UserProfileView

from . import views



urlpatterns = [
    # User registration endpoint
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # User login and token retrieval endpoint
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # User profile view and update (requires token authentication)
    path('profile/', UserProfileView.as_view(), name='user-profile'),


]
