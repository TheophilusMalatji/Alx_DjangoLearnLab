from rest_framework import serializers
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class ActorSerializer(serializers.ModelSerializer):
    """Minimal serializer for the user who triggered the notification."""
    class Meta:
        model = User
        fields = ('id', 'username')

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for reading a user's notifications."""
    actor = ActorSerializer(read_only=True)
    target_post_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id', 'actor', 'verb', 'target_post_id', 
            'read', 'created_at'
        )
        read_only_fields = fields

    def get_target_post_id(self, obj):
        """Returns the ID of the target post if it exists."""
        return obj.target_post.id if obj.target_post else None
