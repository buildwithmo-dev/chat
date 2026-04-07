from rest_framework import serializers
from .models import Messages, ChatGroups, Memberships
from users.models import Profiles # Import your user model

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['id', 'username', 'avatar_url']

class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroups
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    # This nests the sender's info (name/avatar) inside the message JSON
    sender_detail = UserProfileSerializer(source='sender', read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'sender', 'sender_detail', 'group', 'content', 'attachments', 'created_at']
        read_only_fields = ['id', 'created_at']