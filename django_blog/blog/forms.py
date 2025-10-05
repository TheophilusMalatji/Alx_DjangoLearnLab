from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagWidget

#TagWidget() implemented
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email'] 

class PostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = ['title','content','tags']
        widgets = {
            
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title here'}),           
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Write your content here...'}),   
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
        
        }

        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']