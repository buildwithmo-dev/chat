import jwt
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
            jwks_url = (
                f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
            )

            print(f"JWKS URL: {jwks_url}")

            jwks_client = jwt.PyJWKClient(jwks_url)

            signing_key = jwks_client.get_signing_key_from_jwt(token)

            print(f"JWT algorithm: {jwt.get_unverified_header(token).get('alg')}")
            print(f"JWT key ID: {jwt.get_unverified_header(token).get('kid')}")

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256"],
                audience="authenticated",
            )

        except jwt.ExpiredSignatureError as exc:
            print(f"JWT ERROR: expired: {exc}")
            raise exceptions.AuthenticationFailed(
                "Token expired"
            ) from exc

        except jwt.InvalidSignatureError as exc:
            print(f"JWT ERROR: invalid signature: {exc}")
            raise exceptions.AuthenticationFailed(
                "Invalid token signature"
            ) from exc

        except jwt.InvalidAudienceError as exc:
            print(f"JWT ERROR: invalid audience: {exc}")
            raise exceptions.AuthenticationFailed(
                "Invalid token audience"
            ) from exc

        except jwt.InvalidAlgorithmError as exc:
            print(f"JWT ERROR: invalid algorithm: {exc}")
            raise exceptions.AuthenticationFailed(
                "Invalid token algorithm"
            ) from exc

        except jwt.PyJWKClientError as exc:
            print(f"JWKS ERROR: {exc}")
            raise exceptions.AuthenticationFailed(
                f"Unable to retrieve Supabase signing key: {exc}"
            ) from exc

        except jwt.InvalidTokenError as exc:
            print(f"JWT ERROR: {type(exc).__name__}: {exc}")
            raise exceptions.AuthenticationFailed(
                f"Invalid token: {exc}"
            ) from exc

        except Exception as exc:
            print(f"AUTH ERROR: {type(exc).__name__}: {exc}")
            raise exceptions.AuthenticationFailed(
                f"Unable to verify Supabase token: {type(exc).__name__}: {exc}"
            ) from exc

        user_id = payload.get("sub")

        if not user_id:
            raise exceptions.AuthenticationFailed(
                "Invalid token payload"
            )

        try:
            profile, _ = Profiles.objects.get_or_create(id=user_id)
        except Exception as exc:
            print(f"PROFILE ERROR: {type(exc).__name__}: {exc}")
            raise exceptions.AuthenticationFailed(
                "Unable to load user profile"
            ) from exc

        request.supabase_user = payload

        return profile, token