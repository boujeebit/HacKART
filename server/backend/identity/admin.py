from django.contrib import admin
from identity.models import Broker, Integration, Log

admin.site.register(Broker)
admin.site.register(Integration)
admin.site.register(Log)