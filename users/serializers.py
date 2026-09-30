from rest_framework import serializers

from .models import Profiles


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ["id", "username", "bio", "avatar_url", "phone_number", "created_at"]
        read_only_fields = ["id", "created_at", "phone_number"]

    def validate_username(self, value):
        value = (value or "").strip()
        if not value:
            return None  # avoid unique clashes on empty strings
        if len(value) > 40:
            raise serializers.ValidationError("Username too long")
        return value
