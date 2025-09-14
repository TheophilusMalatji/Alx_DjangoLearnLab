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
class UserProile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can change a book"),
            ("can_delete_book", "Can delete a book"),
        ]
class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.name
    
class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name