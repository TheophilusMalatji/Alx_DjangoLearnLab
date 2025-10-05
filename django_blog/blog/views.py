from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm,PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from taggit.models import Tag 
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

    return render(request,'blog/register.html',context)

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

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  
    context_object_name = 'posts'         
    ordering = ['-published_date']

    def get_context_data(self, **kwargs):    
        context = super().get_context_data(**kwargs)       
      
        context['all_comments'] = Comment.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html' 
    fields = ['title', 'content', 'tags']        
    form_class = PostForm 
    
    success_url = reverse_lazy('post-list') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html' 
    success_url = reverse_lazy('post-list')      
    
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    def form_valid(self, form):
       
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.post = post
        response = super().form_valid(form)     
              
        return response

    def get_success_url(self):        
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' 
    
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


    def get_success_url(self):        
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    # Define where to redirect after deletion
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
class PostSearchView(ListView):
        model = Post
        template_name = 'blog/search_results.html'
        context_object_name = 'search_results'
        ordering = ['-published_date']

        def get_queryset(self):     
            query = self.request.GET.get('q')

            if query:            
                queryset = Post.objects.filter(Q(title__icontains=query) |  Q(content__icontains=query) |  Q(tags__name__icontains=query)).distinct()  
            else:
           
                queryset = Post.objects.none() 

            return queryset

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
                                          
            context['query'] = self.request.GET.get('q')
            return context

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Reuse the main post list template
    context_object_name = 'posts'
    ordering = ['-published_date']

    def get_queryset(self): 
        if tag_name:      
              return tag.posts.all().order_by('-published_date')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        # Pass the current tag name to the template for display
        context = super().get_context_data(**kwargs)
        context['current_tag'] = self.kwargs.get('tag_name')
        return context