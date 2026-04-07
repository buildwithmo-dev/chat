from django.db import models
from django.conf import settings 

class ChatGroups(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    group_icon = models.TextField(blank=True, null=True)
    # FIX: Change 'Profiles' to settings.AUTH_USER_MODEL
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_groups'


class Memberships(models.Model):
    id = models.UUIDField(primary_key=True)
    # FIX: Change 'Profiles' to settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(ChatGroups, models.DO_NOTHING, blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    joined_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memberships'

class Messages(models.Model):
    id = models.UUIDField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(ChatGroups, models.DO_NOTHING, blank=True, null=True)
    content = models.TextField()
    attachments = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'


# class Profiles(models.Model):
#     id = models.UUIDField(primary_key=True)
#     username = models.TextField(unique=True, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     avatar_url = models.TextField(blank=True, null=True)
#     phone_number = models.TextField(unique=True, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'profiles'


class Statuses(models.Model):
    id = models.UUIDField(primary_key=True)
    # Change 'Profiles' to settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    media_url = models.TextField()
    caption = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statuses'
