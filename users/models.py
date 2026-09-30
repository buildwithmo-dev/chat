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
        managed = False
        db_table = 'profiles'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.username or str(self.id)