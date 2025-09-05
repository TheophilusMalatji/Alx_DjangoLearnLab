from django.urls import path, include
from relationship_app import views
from relationship_app.views import *
from django.contrib.auth.views import LoginView, LogoutView

# views.register

#LibraryDetailView 



urlpatterns = [
    
    path('books/', views.list_books, name='list_books'),
    path('libraries/', LibraryView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relogout'),name="logout"),
     path('admin/', views.admin_view, name='admin'),
    path('librarian/', views.librarian_view, name='librarian'),
    path('member/', views.member_view, name='member'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
