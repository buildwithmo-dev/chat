from django.db import models


class ChatGroups(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    group_icon = models.TextField(blank=True, null=True)
    created_by_id = models.UUIDField(db_column="created_by", blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat_groups"


class Memberships(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(db_column="user_id", blank=True, null=True)
    group_id = models.UUIDField(db_column="group_id", blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    joined_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "memberships"


class Messages(models.Model):
    id = models.UUIDField(primary_key=True)
    sender_id = models.UUIDField(db_column="sender_id", blank=True, null=True)
    group_id = models.UUIDField(db_column="group_id", blank=True, null=True)
    content = models.TextField()
    attachments = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "messages"


class Statuses(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(db_column="user_id", blank=True, null=True)
    media_url = models.TextField()
    caption = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "statuses"
