from rest_framework import serializers
from .models import Book,Author
from datetime import datetime



class BookSerializer(serializers.ModelSerializer):
    #author_name = serializers.CharField(source='author.name', many=True, read_only=True)
    class Meta:
        model = Book
        fields = '__all__'
    """
    Uses datetime to get current year then compares it to the publication value in the the Book data. If the year is higher than current 
    year then it raises error.
    """
    def validate(self, data):
        current_datetime = datetime.now()
        current_year = current_datetime.year
        if data['publication_year'] > current_year:
            raise serializers.ValidationError("Publication date can not be future date")
        return data
    
class AuthorSerializer(serializers.ModelSerializer):
    """
    Author will now allow for multilpe books to be attached to it. 
    """
    books =BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = '__all__'