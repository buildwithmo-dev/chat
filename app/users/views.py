# users/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profiles
from .serializers import ProfileSerializer # Make sure you have this in serializers.py
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch') # Add this decorator!
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)