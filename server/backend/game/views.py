from django.shortcuts import render
from django.http import HttpResponse
import json, datetime

from identity.models import Platform
# from node.models import Node, Network

'''
localhost:8000/plaform/hook
key need in header
Body: 
{
    team: id
    challenge: id
}
'''

def hook(request):
    if request.method == 'POST':
        if 'key' not in request.headers:
            return HttpResponse(status=401)


        print("Key: ", request.headers['key'])
        if not Platform.objects.filter(key=request.headers['key']):
            return HttpResponse(status=403)

        if request.body:
            payload = json.loads(request.body.decode('utf-8'))
        else:
            return HttpResponse(status=400)
        
        if 'team' in payload and 'challenge' in payload:
            print(payload)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    else:
        return HttpResponse(status=400)