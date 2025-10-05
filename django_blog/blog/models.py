from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here. Here

class Tag(models.Model):  
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

"""
Post model 
"""
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, related_name='posts',  blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"