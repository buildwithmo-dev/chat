import logging

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from users.models import Profiles

logger = logging.getLogger(__name__)
_jwks_client = None


def _get_jwks_client():
    """Module-level singleton so signing keys are cached across requests."""
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = jwt.PyJWKClient(
            f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json",
            cache_keys=True,
            lifespan=3600,
        )
    return _jwks_client


class SupabaseAuthentication(authentication.BaseAuthentication):
    """Authenticate DRF requests with a Supabase access token."""

    def authenticate(self, request):
        header = request.META.get("HTTP_AUTHORIZATION", "")
        if not header.startswith("Bearer "):
            return None

        token = header[7:].strip()
        if not token:
            raise exceptions.AuthenticationFailed("Missing bearer token")
        if not settings.SUPABASE_URL:
            logger.error("SUPABASE_URL is not configured")
            raise exceptions.AuthenticationFailed("Authentication unavailable")

        try:
            alg = jwt.get_unverified_header(token).get("alg")
            if alg == "HS256" and settings.SUPABASE_JWT_SECRET:
                key, algorithms = settings.SUPABASE_JWT_SECRET, ["HS256"]
            else:
                key = _get_jwks_client().get_signing_key_from_jwt(token).key
                algorithms = ["ES256", "RS256"]
            payload = jwt.decode(token, key, algorithms=algorithms, audience="authenticated")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.PyJWKClientError:
            logger.exception("Unable to fetch Supabase signing key")
            raise exceptions.AuthenticationFailed("Unable to verify token")
        except jwt.InvalidTokenError as exc:
            logger.info("Invalid token: %s", type(exc).__name__)
            raise exceptions.AuthenticationFailed("Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        try:
            profile, _ = Profiles.objects.get_or_create(id=user_id)
        except Exception:
            logger.exception("Profile load failed")
            raise exceptions.AuthenticationFailed("Unable to load user profile")

        request.supabase_user = payload
        return profile, token
