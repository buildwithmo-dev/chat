from jose import jwt
from jose.exceptions import JWTError
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles
import requests

SUPABASE_JWKS_URL = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
SUPABASE_ISSUER = f"{settings.SUPABASE_URL}/auth/v1"


def get_jwks():
    try:
        res = requests.get(SUPABASE_JWKS_URL, timeout=5)
        res.raise_for_status()
        data = res.json()

        if "keys" not in data:
            raise exceptions.AuthenticationFailed("Invalid JWKS format")

        return data

    except Exception as e:
        raise exceptions.AuthenticationFailed(f"Failed to fetch JWKS: {str(e)}")


def get_payload(token):
    jwks = get_jwks()

    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")

    if not kid:
        raise exceptions.AuthenticationFailed("Token missing kid")

    key = None
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            key = k
            break

    if not key:
        raise exceptions.AuthenticationFailed(
            f"Public key not found for kid: {kid}"
        )

    try:
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience="authenticated",
            issuer=SUPABASE_ISSUER
        )
    except JWTError as e:
        raise exceptions.AuthenticationFailed(f"Token decode failed: {str(e)}")


class SupabaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        payload = get_payload(token)
        user_id = payload.get("sub")

        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        profile, _ = Profiles.objects.get_or_create(id=user_id)

        return (profile, None)