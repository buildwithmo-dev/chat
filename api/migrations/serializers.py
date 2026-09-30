from rest_framework import serializers

from .models import ChatGroups, Messages


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroups
        fields = ["id", "name", "description", "group_icon", "created_by_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="sender_id", read_only=True)
    text = serializers.CharField(source="content", read_only=True)
    group_id = serializers.UUIDField(read_only=True)
    sender_name = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ["id", "user_id", "sender_name", "sender_avatar", "text",
                  "group_id", "attachments", "created_at"]

    def _profile(self, obj):
        return self.context.get("profiles", {}).get(obj.sender_id)

    def get_sender_name(self, obj):
        p = self._profile(obj)
        return p.username if p else None

    def get_sender_avatar(self, obj):
        p = self._profile(obj)
        return p.avatar_url if p else None


class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=10000, trim_whitespace=True)
    group_id = serializers.UUIDField(required=False, allow_null=True)
    attachments = serializers.JSONField(required=False, allow_null=True)

    def validate_attachments(self, value):
        if value is None:
            return value
        if not isinstance(value, list) or len(value) > 10:
            raise serializers.ValidationError("attachments must be a list of at most 10 items")
        if len(str(value)) > 20000:
            raise serializers.ValidationError("attachments payload too large")
        return value
