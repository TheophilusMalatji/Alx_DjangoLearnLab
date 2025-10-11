from django.urls import path,include
from .views import UserRegistrationView, UserLoginView, UserProfileView
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    # User registration endpoint
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # User login and token retrieval endpoint
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # User profile view and update (requires token authentication)
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    path('', include(router.urls)),
]
