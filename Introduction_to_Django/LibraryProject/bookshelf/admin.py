from . models import Book
from django.contrib import admin

# Register your models here.
@admin.register(Book)
class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')    
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
