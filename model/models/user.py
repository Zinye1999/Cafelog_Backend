from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.model import SoftDeleteModel
from uuid import uuid4

class User(AbstractUser, SoftDeleteModel):
    
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    name = models.CharField(max_length=70, default="")
    details_status = models.TextField(blank=True, null=True)

    profile_picture = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField("self", related_name="+", null=True, blank=True, symmetrical=False)
    followings = models.ManyToManyField("self", related_name="+", null=True, blank=True, symmetrical=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ("email", )
        db_table = "users"
        verbose_name = "user"

    def for_auth(self):
        from model.serializers import UserAuthSerializer
        data = UserAuthSerializer(self).data
        def _map_user(uuids):
            return [str(uid) for uid in uuids]
        return {
            "id": str(self.id),
            "email": self.email,
            "picture": self.profile_picture,
            "name": self.name,
            "followers": _map_user(data.get("followers", [])),
            "followings": _map_user(data.get("followings", []))
        }