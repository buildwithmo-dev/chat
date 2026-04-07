# users/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profiles
from .serializers import ProfileSerializer # Make sure you have this in serializers.py

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # This returns the profile of the person currently logged in via Supabase JWT
        return self.request.user