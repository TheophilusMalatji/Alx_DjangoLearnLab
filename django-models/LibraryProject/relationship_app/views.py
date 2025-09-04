from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def list_books(request):
    books = Book.objects.all()
    context = {list_books:books}
    return render(request,'relationship_app/list_books.html', context )
class LibraryView(ListView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['books'] = self.object.books.all()
        return context

# UserCreationForm()
#relationship_app/register.html
class SignUpView(UserCreationForm):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def is_admin(user):   
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):    
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):    
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')
@user_passes_test(is_member)
def admin_view(request):
    return render(request, 'relationship_app/member_view.html')
@user_passes_test(is_librarian)
def admin_view(request):
    return render(request, 'relationship_app/librarian_view.html')