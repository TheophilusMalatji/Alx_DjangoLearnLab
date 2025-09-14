# your_app_name/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.db.models import Permission
from django.http import HttpResponse




@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return HttpResponse("You have permission")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    
    return HttpResponse("You have permission")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return HttpResponse("You have permission")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse("You have permission")