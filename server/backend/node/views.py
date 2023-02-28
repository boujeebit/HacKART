from django.shortcuts import render
from django.http import HttpResponse
import json, datetime

from identity.models import Integration
from node.models import Node, Network

def heartbeat(request):
    if 'key' not in request.headers:
        return HttpResponse(status=401)

    if not Integration.objects.filter(key=request.headers['key'], type='HB'):
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

    if 'initialized' in payload:
        node.initialized = datetime.datetime.now()
        node.machineid = payload['initialized']['mid']
        if 'heartbeat' in payload['initialized']:
            if payload['initialized']['heartbeat']['enabled']:
                node.heartbeats = True
                node.internval = payload['initialized']['heartbeat']['interval']
            else:
                node.heartbeats = False
        else:
            node.heartbeats = False

        node.save()

        try:
            networking = node.networking
            networking.mac = payload['initialized']['interface']['mac']
            networking.address = payload['initialized']['interface']['lease'][0]
            networking.subnet = payload['initialized']['interface']['lease'][1]
            networking.gateway = payload['initialized']['interface']['lease'][2]
            networking.dns = payload['initialized']['interface']['lease'][3]
        except:
            networking = Network(mac=payload['initialized']['interface']['mac'], 
                address=payload['initialized']['interface']['lease'][0],
                subnet=payload['initialized']['interface']['lease'][1],
                gateway=payload['initialized']['interface']['lease'][2],
                dns=payload['initialized']['interface']['lease'][3],
                node=node)

        networking.save()



    return HttpResponse(status=200)

