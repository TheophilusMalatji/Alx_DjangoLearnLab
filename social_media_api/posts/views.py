from django.shortcuts import render
from .models import Post, Comment, Like
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from django.contrib.auth import get_user_model
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer

CustomUser = get_user_model()


def create_like_notification(post, liker):
    """Creates a notification for the post's author when their post is liked."""
    if post.author != liker:
        Notification.objects.create(
            recipient=post.author,
            actor=liker,
            verb=f"liked your post: \"{post.title[:30]}...\"",
            target_post=post
        )

def create_comment_notification(comment):
    """Creates a notification for the post's author when their post is commented on."""
    # FIX: Corrected typo from comment.posta to comment.post
    post = comment.post
    if post.author != comment.author:
        Notification.objects.create(
            recipient=post.author,
            actor=comment.author,
            verb=f"commented on your post: \"{post.title[:30]}...\"",
            target_post=post)

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Action to like a specific post. Explicitly uses get_object_or_404 and get_or_create."""
        # Explicitly using get_object_or_404 as requested
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Explicitly using Like.objects.get_or_create as requested
        like_obj, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
             return Response({'detail': 'Post already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the notification only if the like was newly created
        create_like_notification(post, user)
        
        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """Action to unlike a specific post. Explicitly uses get_object_or_404."""
        # Explicitly using get_object_or_404 as requested
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Attempt to find and delete the like
        like_qs = Like.objects.filter(post=post, user=user)
        if like_qs.exists():
            like_qs.delete()
            return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Post was not liked.'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """Provides CRUD operations for Comments."""
    # Fetch all comments, ordered by creation time descending (newest first)
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    
    # Permissions: Guests can read. Authenticated users can create (POST).
    # Only the author can edit/delete (PUT/PATCH/DELETE) their own comments.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    pagination_class = StandardResultsPagination
    
    def perform_create(self, serializer):
        """Sets author and creates notification on comment creation."""
        comment = serializer.save(author=self.request.user)
        create_comment_notification(comment)


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides the personalized feed (posts from followed users)."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        """Returns posts from users the current user is following, ordered by creation date."""
        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.none() 
            
        following_users = user.following.all()
        # Filter posts where the author is in the list of users the current user follows
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
