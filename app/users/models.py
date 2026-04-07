from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ProfilesManager(BaseUserManager):
    def create_user(self, id, username, **extra_fields):
        if not id:
            raise ValueError("The ID (UUID from Supabase) must be set")
        user = self.model(id=id, username=username, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, username, **extra_fields):
        # Superuser logic if needed for Django Admin
        return self.create_user(id, username, **extra_fields)

class Profiles(AbstractBaseUser):
    id = models.UUIDField(primary_key=True)
    username = models.TextField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    phone_number = models.TextField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # Required fields for AbstractBaseUser
    password = None 
    last_login = models.DateTimeField(blank=True, null=True)

    objects = ProfilesManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False  # Critical: Supabase still owns this table
        db_table = 'profiles'

    def __str__(self):
        return self.username or str(self.id)