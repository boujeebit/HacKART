from django.shortcuts import render
from django.http import HttpResponse
import json, datetime

from node.models import Node, Heartbeat

def heartbeat(request):
    node = Node.objects.all().first()
    node.heartbeat = datetime.datetime.now()
    node.save()
    return HttpResponse(status=200)

