import jwt
from jwt import InvalidTokenError
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles


class SupabaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        # -----------------------------
        # 1. VERIFY JWT LOCALLY (FAST + SECURE)
        # -----------------------------
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        except InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        user_id = payload.get("sub")

        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        # -----------------------------
        # 2. SYNC USER INTERNALLY (NO SUPABASE CALL)
        # -----------------------------
        user_profile, _ = Profiles.objects.get_or_create(id=user_id)

        # Optional: attach useful metadata from JWT
        request.supabase_user = payload

        return (user_profile, None)