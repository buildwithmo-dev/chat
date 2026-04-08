# users/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profiles
from .serializers import ProfileSerializer # Make sure you have this in serializers.py

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    # Add this so your 'api.post' from React works
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)