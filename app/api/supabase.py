import requests
from django.conf import settings

def get_user_from_token(token):
    res = requests.get(
        f"{settings.SUPABASE_URL}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {token}",
            "apikey": settings.SUPABASE_ANON_KEY
        }
    )

    if res.status_code != 200:
        return None

    return res.json()