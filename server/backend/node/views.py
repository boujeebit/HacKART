from django.shortcuts import render
from django.http import HttpResponse
import json, datetime

from node.models import Node, Heartbeat

def heartbeat(request):
    if 'key' not in request.headers:
        return HttpResponse(status=401)

    if not Heartbeat.objects.filter(key=request.headers['key']):
        return HttpResponse(status=403)

    if request.body:
        payload = json.loads(request.body.decode('utf-8'))
        print(payload)
    else:
        return HttpResponse(status=400)

    if 'id' in payload:
        try:
            node = Node.objects.get(id=payload['id'])
        except:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=400)

    node.heartbeat = datetime.datetime.now()
    node.save()

    return HttpResponse(status=200)

