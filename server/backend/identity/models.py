from django.db import models
from django.contrib.auth.models import User
import uuid

class Integration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=2, choices=[('PF', 'Platform'), ('HB', 'Heartbeat')], null=False)

    key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    hint = models.CharField(max_length=128, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="integrations")

    def __str__(self):
        return self.name

# Logs
class Log(models.Model):
    code = models.IntegerField(null=False, blank=False)
    message = models.CharField(max_length=128, null=False, blank=False)
    payload = models.CharField(max_length=1024, null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    source = models.CharField(max_length=64, null=True, blank=True)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name="logs")

# Used for MQTT connection
class Broker(models.Model):
    endpoint = models.CharField(max_length=256, null=False, blank=False)
    port = models.IntegerField(default=8443, null=False, blank=False)

    def __str__(self):
        return self.endpoint