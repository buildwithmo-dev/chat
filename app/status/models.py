import uuid
from django.db import models
from django.conf import settings

class Status(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media_url = models.TextField()
    caption = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField()