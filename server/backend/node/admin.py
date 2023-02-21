from django.contrib import admin
from node.models import Node, Network, Heartbeat

admin.site.register(Node)
admin.site.register(Network)
admin.site.register(Heartbeat)
