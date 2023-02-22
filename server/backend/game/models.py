from django.db import models
import uuid

from node.models import Node

class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # This is the ID field for challenge in the external CTF platform
    external_id = models.CharField(max_length=256, unique=True, null=False)
    name = models.CharField(max_length=256, unique=True, null=True, blank=True)

    class TrafficLight(models.IntegerChoices):
        green  = 1
        yellow = 2
        red    = 3

    balloon = models.IntegerField(choices=TrafficLight.choices, unique=True)

class Solve(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="solves")
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="solves")
    time = models.DateTimeField(null=False)