from django.contrib import admin
from node.models import Node, Heartbeat

admin.site.register(Node)
admin.site.register(Heartbeat)
