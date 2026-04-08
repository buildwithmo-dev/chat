from jose import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import Profiles # Import your Profiles model

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
            
            # Since Supabase uses HS256 for the Project API Key, 
            # we can decode it directly using your JWT Secret.
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
            
            user_id = payload.get('sub')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Token validation failed: {str(e)}')

        try:
            # We return the Profile object. 
            # DRF will treat this as 'request.user'
            user_profile = Profiles.objects.get(id=user_id)
            return (user_profile, None) 
        except Profiles.DoesNotExist:
            raise exceptions.AuthenticationFailed('User profile not found in public.profiles')