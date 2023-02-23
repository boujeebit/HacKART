from django.contrib import admin
from identity.models import Platform, Heartbeat, Broker

admin.site.register(Platform)
admin.site.register(Heartbeat)
admin.site.register(Broker)