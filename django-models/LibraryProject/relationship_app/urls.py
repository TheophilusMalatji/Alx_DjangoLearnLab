from django.urls import path, include
from relationship_app import views
from relationship_app.views import *
from django.contrib.auth.views import LoginView, LogoutView

#LibraryDetailView



urlpatterns = [
    
    path('books/', views.list_books, name='list_books'),
    path('libraries/', LibraryView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relogout'),name="logout")
]
