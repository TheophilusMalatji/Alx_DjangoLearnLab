from rest_framework import status, viewsets,filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import Post, Comment
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..posts.permissions import IsOwnerOrReadOnly

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, PostSerializer,CommentSerializer

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
# --- Pagination Configuration ---
class StandardResultsPagination(PageNumberPagination):
    """Sets standard page size and max page size for results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# --- ViewSets for CRUD Operations ---

class PostViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Posts.
    Permissions: Read-only for all, Write/Edit/Delete only for the author.
    Pagination and Search are implemented.
    """
    # Fetch all posts, ordered by creation time descending (newest first)
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    
    # Permissions: Guests can read. Authenticated users can create (POST).
    # Only the author can edit/delete (PUT/PATCH/DELETE) their own posts.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    pagination_class = StandardResultsPagination
    
    # Enable searching by title and content fields
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        """When creating a post, automatically set the author to the request user."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Comments.
    Permissions: Read-only for all, Write/Edit/Delete only for the author.
    Pagination is implemented.
    """
    # Fetch all comments, ordered by creation time descending (newest first)
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    
    # Permissions: Guests can read. Authenticated users can create (POST).
    # Only the author can edit/delete (PUT/PATCH/DELETE) their own comments.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    pagination_class = StandardResultsPagination
    
    def perform_create(self, serializer):
        """When creating a comment, automatically set the author to the request user."""
        serializer.save(author=self.request.user)