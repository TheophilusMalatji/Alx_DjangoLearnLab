from django import forms
from models import Book


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields =['author','title','publication_year']