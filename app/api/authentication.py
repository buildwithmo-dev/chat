from jose import jwt
from jose.exceptions import JWTError, JOSEError
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles
import requests

SUPABASE_JWKS_URL = f"{settings.SUPABASE_URL}/auth/v1/keys"
SUPABASE_ISSUER = f"{settings.SUPABASE_URL}/auth/v1"


def get_jwks():
    try:
        return requests.get(SUPABASE_JWKS_URL, timeout=5).json()
    except Exception:
        raise exceptions.AuthenticationFailed("Failed to fetch JWKS")


def get_payload(token):
    jwks = get_jwks()

    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")

    if not kid:
        raise exceptions.AuthenticationFailed("Invalid token header (no kid)")

    key = None
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            key = k
            break

    if not key:
        raise exceptions.AuthenticationFailed("Public key not found")

    try:
        return jwt.decode(
            token,
            key,
            algorithms=[headers.get("alg")],
            audience="authenticated",
            issuer=SUPABASE_ISSUER
        )
    except (JWTError, JOSEError, Exception) as e:
        raise exceptions.AuthenticationFailed(f"Token validation failed: {str(e)}")


class SupabaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        payload = get_payload(token)
        user_id = payload.get('sub')

        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        user_profile, _ = Profiles.objects.get_or_create(id=user_id)

        return (user_profile, None)