from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from users.models import Profiles
from .serializers import ProfileSerializer
from jose import JWTError
import requests

SUPABASE_JWKS_URL = f"{settings.SUPABASE_URL}/auth/v1/keys"


def decode_token(token):
    jwks = requests.get(SUPABASE_JWKS_URL).json()

    return jwt.decode(
        token,
        jwks,
        algorithms=["RS256"],
        audience="authenticated"
    )


class ProfileDetailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "No token provided"}, status=401)

        token = auth_header.split(' ')[1]

        try:
            payload = decode_token(token)
            supabase_user_id = payload.get('sub')
        except Exception as e:
            return Response({"error": f"Token invalid: {str(e)}"}, status=403)

        profile, created = Profiles.objects.update_or_create(
            id=supabase_user_id,
            defaults={
                'username': request.data.get('username'),
                'bio': request.data.get('bio', ''),
            }
        )

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        if not request.user:
            return Response({"error": "Not authenticated"}, status=401)

        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)