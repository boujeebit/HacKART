from django.contrib import admin
from identity.models import Platform, Heartbeat

admin.site.register(Platform)
admin.site.register(Heartbeat)