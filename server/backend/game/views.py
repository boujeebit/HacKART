from django.shortcuts import render
from django.http import HttpResponse
import json, datetime

from identity.models import Integration
# from node.models import Node, Network
from team.models import Team
from game.models import Challenge, Solve

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
      return HttpResponse(status=500)
  else:
    return HttpResponse(status=400)
    

  # Team Build
  if 'team' in payload:
    if 'type' not in payload['team'] or payload['team']['type'].lower() not in ['create', 'update', 'delete']:
      return HttpResponse(status=400)

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
      return HttpResponse(status=400)

    try:
      team = Team.objects.get(external_id=payload['solve']['team'])
    except:
      return HttpResponse(status=404)

    try:
      challenge = Challenge.objects.get(external_id=payload['solve']['challenge'])
    except:
      return HttpResponse(status=404)

    try:
      node = team.node
    except:
      return HttpResponse(status=500)

    # Check if node or team has this solve.

    # Send Solve to AWS

    try:
      solve = Solve(challenge=challenge, node=node)
      solve.save()
      return HttpResponse(status=200)
    except:
      return HttpResponse(status=500)

      
  # If not team or solve
  else:
    return HttpResponse(status=400)
    