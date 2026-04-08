from jose import jwt, JWTError
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles
import requests

SUPABASE_JWKS_URL = f"{settings.SUPABASE_URL}/auth/v1/keys"


def get_payload(token):
    jwks = requests.get(SUPABASE_JWKS_URL).json()

    return jwt.decode(
        token,
        jwks,
        algorithms=["RS256"],
        audience="authenticated"
    )


class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = get_payload(token)
            user_id = payload.get('sub')
        except JWTError as e:
            raise exceptions.AuthenticationFailed(
                f'Token validation failed: {str(e)}'
            )

        try:
            user_profile = Profiles.objects.get(id=user_id)
            return (user_profile, None)
        except Profiles.DoesNotExist:
            return None