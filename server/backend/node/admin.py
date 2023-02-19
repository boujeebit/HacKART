from django.contrib import admin
from node.models import Node, Networking, Heartbeat

admin.site.register(Node)
admin.site.register(Networking)
admin.site.register(Heartbeat)
