from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from posts.models import Post # Link to the Post model

User = get_user_model()

class Notification(models.Model):
    """Represents a notification for a user based on social actions."""
    # The user who receives the notification
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    # The user who performed the action (e.g., the liker, the follower)
    actor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='actions_performed'
    )
    # A description of the action
    verb = models.CharField(max_length=255) 
    
    # Optional link to the relevant post
    target_post = models.ForeignKey(
        Post, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient.username}: {self.actor.username} {self.verb}"
