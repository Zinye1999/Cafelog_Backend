from django.db import models
import secrets
from django.utils import timezone
from datetime import timedelta

from uuid import uuid4

def generate_token():
    return secrets.token_hex(32)

def exp_time(minutes=15):
    return timezone.now() + timedelta(minutes=minutes)

class TemporaryPassword(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    password = models.CharField(max_length=43, null=False, default=generate_token)
    for_user = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    expired = models.DateTimeField(default=exp_time)

    class Meta:
        db_table = "temporary_passwords"
        verbose_name = "temporary_password"