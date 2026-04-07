# users/serializers.py
from rest_framework import serializers
from .models import Profiles

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['id', 'username', 'bio', 'avatar_url', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at'] # These are handled by Supabase/Postgres