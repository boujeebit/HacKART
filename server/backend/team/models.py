from django.db import models
import uuid

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # This is the ID field for challenge in the external CTF platform
    external_id = models.CharField(max_length=256, unique=True, null=False)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name
