from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Django handles username, email, password by default
    bio = models.TextField(null=True, blank=True)
    avatar_url = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)