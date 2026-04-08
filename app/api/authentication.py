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
            # CRITICAL: Specify HS256 to stop the "alg not allowed" error
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"], 
                audience="authenticated"
            )
            user_id = payload.get('sub')
        except JWTError as e:
            raise exceptions.AuthenticationFailed(f'Token validation failed: {str(e)}')

        try:
            # Standard flow for logged-in users
            user_profile = Profiles.objects.get(id=user_id)
            return (user_profile, None)
        except Profiles.DoesNotExist:
            # Registration flow: Return None so the View can create the profile
            return None