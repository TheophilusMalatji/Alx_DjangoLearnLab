from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser

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
        """Create and return a new user instance, setting the hashed password."""
        # Pop the extra password field before saving
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=password,
            bio=validated_data.get('bio', '')
        )
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
