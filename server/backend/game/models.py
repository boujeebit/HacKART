from django.db import models
import uuid

from node.models import Node
from team.models import Team

class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # This is the ID field for challenge in the external CTF platform
    external_id = models.CharField(max_length=256, unique=True, null=False)
    name = models.CharField(max_length=256, unique=True, null=True, blank=True)

    balloon = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], unique=True)

    def __str__(self) -> str:
        return self.name

class Solve(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="solves")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="solves")

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s)" % (self.challenge.name, self.team.name)