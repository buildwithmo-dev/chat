# users/models.py
from django.db import models

class Profiles(models.Model):
    # This ID matches the UUID from Supabase auth.users
    id = models.UUIDField(primary_key=True, editable=False)
    username = models.TextField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    phone_number = models.TextField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        managed = False  # Django won't try to create/modify this table
        db_table = 'profiles' # Points to the table in your SQL schema

    def __str__(self):
        return self.username or str(self.id)