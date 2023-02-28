from django.contrib import admin
from identity.models import Broker, Integration

admin.site.register(Broker)
admin.site.register(Integration)