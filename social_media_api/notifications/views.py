from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from .serializers import NotificationSerializer
from posts.views import StandardResultsPagination # Reuse existing pagination


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only access to a user's notifications and actions to mark them as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        """Returns notifications for the current authenticated user."""
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Action to mark a specific notification as read."""
        try:
            notification = self.get_queryset().get(pk=pk)
        except Notification.DoesNotExist:
            return Response({'detail': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)
            
        if not notification.read:
            notification.read = True
            notification.save()
            return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)
            
        return Response({'detail': 'Notification was already read.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Action to mark all unread notifications for the current user as read."""
        unread_notifications = self.get_queryset().filter(read=False)
        count = unread_notifications.update(read=True)
        return Response(
            {'detail': f'Marked {count} notifications as read.'}, 
            status=status.HTTP_200_OK
        )
