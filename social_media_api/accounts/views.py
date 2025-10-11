from rest_framework import status, viewsets,filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

CustomUser = get_user_model()

class UserRegistrationView(APIView):
    """Handles user registration and returns a token."""
    permission_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create user
            user = serializer.save()

            # Create or retrieve token for the new user
            token, created = Token.objects.get_or_create(user=user)

            # Return success message, user data, and the token
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """Handles user login, authenticates, and returns the user's token."""
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Create or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            
            # Use the profile serializer to return clean user data
            user_data = UserProfileSerializer(user).data

            return Response({
                'user': user_data,
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Handles retrieving and updating the authenticated user's profile."""
    # Enforces token authentication for this endpoint
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the profile data for the authenticated user."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update the profile data for the authenticated user (bio and profile_picture)."""
        # Pass request.user as the instance to update
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
