from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json, datetime, requests

from identity.models import Integration
# from node.models import Node, Network
from team.models import Team
from game.models import Challenge, Solve
from identity.models import Broker

'''
localhost:8000/plaform/hook
key need in header
Body: 
{
    team: id
    challenge: id
}
'''

def hook(request, id=None):
  if request.method != 'POST':
    return HttpResponse(status=500)

  # Authenticate Hook
  try:
    integration = Integration.objects.get(id=id, type='PF')
  except:
    return HttpResponse(status=404)

  if 'key' not in request.headers:
    return HttpResponse(status=401)

  if str(integration.key) != request.headers['key']:
    return HttpResponse(status=403)
  # End Authenticate Hook

  if request.body:
    try:
      payload = json.loads(request.body.decode('utf-8'))
    except:
      return JsonResponse({"message": "The payload provided was malformed."}, status=500)
  else:
    return JsonResponse({"message": "No payload was provided in request."}, status=400)
    

  # Team Build
  if 'team' in payload:
    if 'type' not in payload['team'] or payload['team']['type'].lower() not in ['create', 'update', 'delete']:
      return JsonResponse({"message": "Payload type must be String of ['create', 'update', 'delete']"}, status=400)

    # Create Team
    if payload['team']['type'].lower() == 'create':
      if 'id' in payload['team'] and 'name' in payload['team']:
        try:
          team = Team(external_id=payload['team']['id'], name=payload['team']['name'], integration=integration)
          team.save()
          return HttpResponse(status=200)
        except:
          return HttpResponse(status=500)
      else:
        return HttpResponse(status=400)

    # Update Team
    if payload['team']['type'].lower() == 'update':
      if 'id' in payload['team'] and 'name' in payload['team']:
        try:
          team = Team.objects.get(external_id=payload['team']['id'])
        except:
          return HttpResponse(status=404)
        
        try:
          team.name = payload['team']['name']
          team.save()
          return HttpResponse(status=200)
        except:
          return HttpResponse(status=500)
      else:
        return HttpResponse(status=400)

    # Delete Team
    if payload['team']['type'].lower() == 'delete':
      if 'id' in payload['team']:
        try:
          team = Team.objects.get(external_id=payload['team']['id'])
        except:
          return HttpResponse(status=404)

        try:
          team.delete()
          return HttpResponse(status=200)
        except:
          return HttpResponse(status=500)

  # Solve
  elif 'solve' in payload:
    if 'team' not in payload['solve'] or 'challenge' not in payload['solve']:
      return JsonResponse({"message": "team or challenge not provided in payload."}, status=400)

    try:
      team = Team.objects.get(external_id=payload['solve']['team'])
    except:
      return JsonResponse({"message": "No team exist with that ID."},status=404)

    try:
      challenge = Challenge.objects.get(external_id=payload['solve']['challenge'])
    except:
      return JsonResponse({"message": "No challenge exist with that ID."}, status=404)

    try:
      node = team.node
    except:
      return HttpResponse({"message": "Team is not assigned to a node."}, status=500)

    # Check if node or team has this solve.

    # Check if Team has solved this challenge
    try:
      Solve.objects.get(challenge=challenge, team=team)
      return JsonResponse({"message": "Team already solved this challenge."}, status=500)
    except:
      pass

    if node.state:
      if node.state[challenge.balloon]:
        return JsonResponse({"message": "Node state for balloon %s is reporting as inactive." % (challenge.balloon)}, status=500)
      else:
        print("Ready pop")

        # Send command to AWS
        try:
          broker = Broker.objects.all().first()
        except:
          return JsonResponse({"message": "No broker configured."}, status=500)
        
        if not broker:
          return JsonResponse({"message": "No broker configured."}, status=500)
        
        publish_url = 'https://%s:%i/topics/hackart/%s?qos=1' % (broker.endpoint, broker.port, node.id)
        publish_msg = {"type": "pop", "state": node.state}

        publish = requests.request('POST',
          publish_url,
          data=json.dumps(publish_msg),
          cert=['/root/certificate.pem.crt', '/root/private.pem.key'])

        if publish.status_code != 200:
          return JsonResponse({"message": "Error with request to AWS."}, status=500)

    else:
      return JsonResponse({"message": "Node is in an unknow state. Cannot complete this request."}, status=500)


    try:
      solve = Solve(challenge=challenge, team=team)
      solve.save()
      return JsonResponse({"message": "Success."}, status=200)
    except:
      return JsonResponse({"message": "Failed to add solved challenge."}, status=500)

      
  # If not team or solve
  else:
    return JsonResponse({"message": "Payload is not a Team or Solve object."}, status=400)
    