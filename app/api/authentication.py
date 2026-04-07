import jwt
import requests
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
            
            # 1. Fetch the public keys from Supabase dynamically
            # Replace 'your-project-id' with your actual Supabase project ID
            jwks_url = f"https://xxuelagumqjmytaacjgg.supabase.co/auth/v1/.well-known/jwks.json"
            jwks_client = jwt.PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            # 2. Decode using the dynamic key
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256"],
                audience="authenticated"
            )
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Token validation failed: {str(e)}')

        user_id = payload.get('sub')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User profile not found')

        return (user, token)