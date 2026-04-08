# api/authentication.py
from jose import jwt, JWTError
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"], # This MUST match the Supabase setting
                audience="authenticated"
            )
            user_id = payload.get('sub')
        except JWTError as e:
            raise exceptions.AuthenticationFailed(f'Token validation failed: {str(e)}')

        try:
            # This is fine for GET/PATCH requests once the user is registered
            user_profile = Profiles.objects.get(id=user_id)
            return (user_profile, None)
        except Profiles.DoesNotExist:
            # We return None here so that the View can handle registration
            return None