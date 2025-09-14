from django.db import models
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from .managers import CustomUserManager
from django.conf import settings
# Create your models here.
# class UserProfile(models.Model):

class CustomUser(AbstractUser):

    date_of_birth = models.DateField()
    profile_photo = models.ImageField()
    objects = CustomUserManager()
    def __str__(self):
        return self.username

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField

    def __str__(self):
        return self.name
    
