from django.urls import path
from .views import list_books
from .views import LibraryView
from . import views



urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('libraries/', views.LibraryView.as_view(), name='library_detail'),
]
