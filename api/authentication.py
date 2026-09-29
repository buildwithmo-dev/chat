import jwt
from jwt import InvalidTokenError
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles


class SupabaseAuthentication(authentication.BaseAuthentication):
    """Authenticate Django REST requests with a Supabase access token."""

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            raise exceptions.AuthenticationFailed("Missing bearer token")

        if not settings.SUPABASE_JWT_SECRET:
            raise exceptions.AuthenticationFailed("Supabase JWT secret is not configured")

        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        except InvalidTokenError as exc:
            raise exceptions.AuthenticationFailed("Invalid or expired token") from exc

        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        try:
            profile, _ = Profiles.objects.get_or_create(id=user_id)
        except Exception as exc:
            raise exceptions.AuthenticationFailed("Unable to load user profile") from exc

        request.supabase_user = payload
        return profile, token
