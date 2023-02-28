from django.db import models
import uuid

from identity.models import Integration

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # This is the ID field for challenge in the external CTF platform
    external_id = models.CharField(max_length=256, unique=True, null=False)
    name = models.CharField(max_length=128, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    integration = models.ForeignKey(Integration, null=True, on_delete=models.CASCADE, related_name="teams")

    def __str__(self) -> str:
        return self.name
