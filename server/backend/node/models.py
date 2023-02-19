from django.db import models
import uuid

from team.models import Team

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    mac = models.CharField(max_length=17, unique=True, null=True, blank=True)
    heartbeat = models.DateTimeField(null=True, blank=True)
    internval = models.IntegerField(null=True, blank=True, default=60)

    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name="node")

# Used for Heartbeat Proxy
class Heartbeat(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    # ip 

    def __str__(self) -> str:
        return self.key