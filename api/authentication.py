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

        if not settings.SUPABASE_URL:
            raise exceptions.AuthenticationFailed(
                "Supabase URL is not configured"
            )

        try:
            # Supabase publishes the public keys used to verify JWTs.
            jwks_url = (
                f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
            )

            jwks_client = jwt.PyJWKClient(jwks_url)

            # Select the public key matching the JWT's `kid`.
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256"],
                audience="authenticated",
            )

        except jwt.ExpiredSignatureError as exc:
            raise exceptions.AuthenticationFailed(
                "Token expired"
            ) from exc

        except jwt.InvalidSignatureError as exc:
            raise exceptions.AuthenticationFailed(
                "Invalid token signature"
            ) from exc

        except jwt.InvalidTokenError as exc:
            raise exceptions.AuthenticationFailed(
                f"Invalid token: {str(exc)}"
            ) from exc

        except Exception as exc:
            raise exceptions.AuthenticationFailed(
                "Unable to verify Supabase token"
            ) from exc

        user_id = payload.get("sub")

        if not user_id:
            raise exceptions.AuthenticationFailed(
                "Invalid token payload"
            )

        try:
            profile, _ = Profiles.objects.get_or_create(id=user_id)
        except Exception as exc:
            raise exceptions.AuthenticationFailed(
                "Unable to load user profile"
            ) from exc

        request.supabase_user = payload

        return profile, token