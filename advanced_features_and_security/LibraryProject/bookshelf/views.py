from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Book
from django.db.models import Permission
# Create your views here.
def book_list(request):
    if not request.user.has_perm('your_app_name.can_view'):
        return HttpResponseForbidden("You do not have permission to view this page.")
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# Create a new book
def create_book(request):
    if not request.user.has_perm('your_app_name.can_create'):
        return HttpResponseForbidden("You do not have permission to create books.")
    # ... logic to handle form submission and create a new book
    return redirect('book_list')

# Edit an existing book
def edit_book(request, pk):
    if not request.user.has_perm('your_app_name.can_edit'):
        return HttpResponseForbidden("You do not have permission to edit this book.")
    book = get_object_or_404(Book, pk=pk)
    # ... logic to handle form submission and edit the book
    return redirect('book_list')

# Delete a book
def delete_book(request, pk):
    if not request.user.has_perm('your_app_name.can_delete'):
        return HttpResponseForbidden("You do not have permission to delete this book.")
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')