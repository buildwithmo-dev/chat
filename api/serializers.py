from rest_framework import serializers
from .models import Messages, ChatGroups
from users.models import Profiles


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ["id", "username", "avatar_url"]


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroups
        fields = ["id", "name", "description", "group_icon", "created_by_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="sender_id", read_only=True)
    text = serializers.CharField(source="content", read_only=True)
    group_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Messages
        fields = ["id", "user_id", "text", "group_id", "attachments", "created_at"]


class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=10000, trim_whitespace=True)
    group_id = serializers.UUIDField(required=False, allow_null=True)
    attachments = serializers.JSONField(required=False, allow_null=True)
