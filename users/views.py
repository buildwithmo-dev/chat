from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profiles
from .serializers import ProfileSerializer


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profiles.objects.get(id=request.user.id)
        except Profiles.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        return Response(ProfileSerializer(profile).data)

    def post(self, request):
        # Partial update: only fields actually sent are changed.
        # Avatars: upload to Supabase Storage from the client, then send avatar_url.
        profile, created = Profiles.objects.get_or_create(id=request.user.id)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201 if created else 200)

    put = patch = post
