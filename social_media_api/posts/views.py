from django.shortcuts import render
from accounts.models import Post, Comment
from ..posts.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, viewsets
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, CommentSerializer

CustomUser = get_user_model()

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