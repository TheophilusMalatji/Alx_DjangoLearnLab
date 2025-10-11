from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import authenticate, get_user_model # Added get_user_model
from accounts.serializers import AuthorSerializer



class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment models.
    Author is read-only and uses the nested AuthorSerializer.
    """
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id', 
            'post', # Expose 'post' ID for creation/association
            'author', 
            'content', 
            'created_at', 
            'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        """
        Ensures the 'author' is automatically set to the authenticated user 
        when a new comment is created.
        """
        # The author must be passed into the serializer context from the view (self.context['request'].user)
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post models.
    Author is read-only and includes a count of related comments.
    """
    author = AuthorSerializer(read_only=True)
    # Read-only field to display the number of comments on the post
    comment_count = serializers.SerializerMethodField()
    
    # Nested comments are often too much data for a list view, but useful for a detail view.
    # We will keep it simple and just show the count for now.

    class Meta:
        model = Post
        fields = (
            'id', 
            'author', 
            'title', 
            'content', 
            'created_at', 
            'updated_at',
            'comment_count'
        )
        read_only_fields = ('created_at', 'updated_at', 'comment_count')
    
    def get_comment_count(self, obj):
        """Returns the number of comments associated with this post."""
        # This relies on the 'related_name'='comments' defined in the Comment model
        return obj.comments.count()
    
    def create(self, validated_data):
        """
        Ensures the 'author' is automatically set to the authenticated user 
        when a new post is created.
        """
        # The author must be passed into the serializer context from the view (self.context['request'].user)
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)