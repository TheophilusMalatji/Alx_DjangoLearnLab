from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model # Added get_user_model
from .models import CustomUser, Post, Comment

# Use get_user_model for explicit access to the configured user model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'bio')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, data):
        """Validate that passwords match."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        """
        Create and return a new user instance, setting the hashed password,
        and immediately generating an authentication token, as requested.
        """
        # Pop the extra password field before saving
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Using get_user_model().objects.create_user as requested
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=password,
            bio=validated_data.get('bio', '')
        )
        
        # Creating the Token here as requested
        Token.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login and token retrieval."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        """Authenticate user based on username and password."""
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing and updating user profile data."""
    # Add a read-only field for follower count
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        # Exclude sensitive fields like password
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'follower_count')
        read_only_fields = ('id', 'username', 'email', 'followers', 'follower_count') # Only bio and profile_picture are editable here

    def get_follower_count(self, obj):
        """Returns the count of users following this user."""
        return obj.followers.count()

class AuthorSerializer(serializers.ModelSerializer):
    """Minimal serializer for displaying user information related to posts/comments."""
    class Meta:
        model = CustomUser
        # Only expose safe, identifying fields
        fields = ('id', 'username', 'profile_picture')
        read_only_fields = fields

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
