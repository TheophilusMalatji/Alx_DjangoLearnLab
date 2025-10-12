from django.urls import path
from . import views

urlpatterns = [
    # Route for fetching user's notifications
    path('', views.NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    
    # Route for marking a specific notification as read
    path('<int:pk>/read/', views.NotificationViewSet.as_view({'post': 'mark_as_read'}), name='notification-read'),
]
