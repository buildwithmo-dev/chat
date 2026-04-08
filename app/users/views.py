from rest_framework import generics, status
from rest_framework.permissions import AllowAny # Import AllowAny
from rest_framework.response import Response
from .models import Profiles
from .serializers import ProfileSerializer
from api.authentication import SupabaseAuthentication # Import your auth class
from jose import jwt
from django.conf import settings

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    # CHANGE THIS: Use AllowAny so the 'register/' endpoint can be reached 
    # even before the Profiles row is created.
    permission_classes = [AllowAny] 

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        # 1. Manually verify the Supabase Token since we are using AllowAny
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return Response({"detail": "No token provided"}, status=401)
        
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token, 
                settings.SUPABASE_JWT_SECRET, 
                algorithms=["HS256"], 
                audience="authenticated"
            )
            supabase_user_id = payload.get('sub')
        except Exception as e:
            return Response({"detail": f"Token invalid: {str(e)}"}, status=403)

        # 2. Use 'update_or_create' to handle the registration
        # This matches the 'sub' from the token to the 'id' in your Profiles model
        profile, created = Profiles.objects.update_or_create(
            id=supabase_user_id,
            defaults={
                'username': request.data.get('username'),
                'bio': request.data.get('bio', ''),
            }
        )

        # 3. Handle Avatar if present
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()

        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)