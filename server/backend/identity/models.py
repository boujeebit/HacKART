from django.db import models
import uuid

# Used for intergrations with CTF Platforms
class Platform(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)

    hint = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

# Used for Heartbeat Proxy
class Heartbeat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)

    hint = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name