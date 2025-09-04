from django.shortcuts import render
from django.views.generic import ListView
from .models import Library

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {list_books:books}
    return render(request,'relationship_app/list_books.html', context )
class LibraryView(ListView):
    model = Library
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['books'] = self.object.books.all()
        return context