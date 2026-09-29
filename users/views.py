from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Profiles
from .serializers import ProfileSerializer


class ProfileDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # ✅ comes from SupabaseAuthentication

        profile, _ = Profiles.objects.update_or_create(
            id=user.id,
            defaults={
                "username": request.data.get("username"),
                "bio": request.data.get("bio", "")
            }
        )

        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
            profile.save()

        return Response(ProfileSerializer(profile).data, status=201)

    def get(self, request):
        user = request.user

        try:
            profile = Profiles.objects.get(id=user.id)
        except Profiles.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        return Response(ProfileSerializer(profile).data)