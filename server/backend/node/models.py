from django.db import models
import uuid

from team.models import Team

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    machineid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    name = models.CharField(max_length=128, unique=True, null=True, blank=True)

    heartbeats  = models.BooleanField(null=True, blank=True)
    initialized = models.DateTimeField(null=True, blank=True)
    heartbeat = models.DateTimeField(null=True, blank=True)
    internval = models.IntegerField(null=True, blank=True)

    state = models.JSONField(null=True, blank=True, default=None)
    team = models.OneToOneField(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name="node")


    def __str__(self) -> str:
        return self.name

class Network(models.Model):
    mac = models.CharField(max_length=17, unique=True, null=False, blank=False)
    ssid = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=17, null=True, blank=True)
    subnet  = models.CharField(max_length=17, null=True, blank=True)
    gateway = models.CharField(max_length=17, null=True, blank=True)
    dns = models.CharField(max_length=17, null=True, blank=True)

    node = models.OneToOneField(Node, on_delete=models.CASCADE, related_name="networking")

class ROM(models.Model):
    key = models.CharField(max_length=64, null=True, blank=True)

class Player(models.Model):
    player = models.CharField(max_length=2, choices=[('P1', 'P1'), ('P3', 'P2'), ('P3', 'P3'), ('P4', 'P4')])

    rom = models.ForeignKey(ROM, null=False, on_delete=models.CASCADE, related_name="players")
    node = models.OneToOneField(Node, on_delete=models.CASCADE, related_name="player")