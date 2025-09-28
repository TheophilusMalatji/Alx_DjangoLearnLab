from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

"""
router = DefaultRouter()
router.register(r'books_all', BookListView, basename='book_all')
router.register(r'books_detail', BookDetailView, basename='book_detail')
router.register(r'books_create', BookCreateView, basename='book_create')
router.register(r'books_update', BookUpdateView, basename='book_update')
router.register(r'books_delete', BookDeleteView, basename='book_delete')
"""

urlpatterns = [
    path('books/',BookListView.as_view(), name="books"),
    path('books/create',BookCreateView.as_view(), name="book-create"),
    path('books/delete',BookDeleteView.as_view(), name="book-delete"),
    path('books/update',BookUpdateView.as_view(), name="book-update"),
]

