from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def registation(request):
    """
    1. Uses a custom form made from django UserCreation form as a base
    2. Use POST method to save information given in registration form.
    3. Uses registration html template and feeds in CustomUserCreationForm as context for the template
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {'form':form}

    return render(request,'blog/registration.html',context)

@login_required 
def profile(request):
    """
    1.This function takes a request from the browser if the request is a POST method then it updates the email address if the form data is valid
    2. If user is not signed in they wont be able to see the profile view
    """
   
    if request.method == 'POST':        
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    
    else:       
        form = UserUpdateForm(instance=request.user)

    
    context = {'form':form}
    
  
    return render(request, 'blog/user_profile.html', context)