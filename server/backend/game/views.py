from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json, datetime, requests

from identity.models import Integration
from node.models import ROM, Player
from team.models import Team
from game.models import Challenge, Solve
from identity.models import Broker, Log

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
    # log = Log(code=500, message="Not a POST request.")
    # log.save()
    return HttpResponse(status=500)

  # Authenticate Hook
  try:
    integration = Integration.objects.get(id=id, type='PF')
  except:
    # log = Log(code=404, message="No integration found.")
    # log.save()
    return HttpResponse(status=404)

  if 'key' not in request.headers:
    # log = Log(code=401, message="No key in header.")
    # log.save()
    return HttpResponse(status=401)

  if str(integration.key) != request.headers['key']:
    # log = Log(code=402, message="Invalid key.")
    # log.save()
    return HttpResponse(status=403)
  # End Authenticate Hook

  if request.body:
    try:
      payload = json.loads(request.body.decode('utf-8'))
    except:
      log = Log(code=500, message="The payload provided was malformed.", integration=integration)
      log.save()
      return JsonResponse({"message": "The payload provided was malformed."}, status=500)
  else:
    log = Log(code=400, message="No payload was provided in request.", integration=integration)
    log.save()
    return JsonResponse({"message": "No payload was provided in request."}, status=400)
    

  # Team Build
  if 'team' in payload:
    if 'type' not in payload['team'] or payload['team']['type'].lower() not in ['create', 'update', 'delete']:
      log = Log(code=400, message="Payload type must be String of ['create', 'update', 'delete']", integration=integration)
      log.save()
      return JsonResponse({"message": "Payload type must be String of ['create', 'update', 'delete']"}, status=400)

    # Create Team
    if payload['team']['type'].lower() == 'create':
      if 'id' in payload['team'] and 'name' in payload['team']:
        try:
          team = Team(external_id=payload['team']['id'], name=payload['team']['name'], payload=payload, integration=integration)
          team.save()
          log = Log(code=200, message="Success.", integration=integration)
          log.save()
          return JsonResponse({"message": "Success."},status=200)
        except:
          log = Log(code=500, message="Failed to create team locally.", integration=integration)
          log.save()
          return JsonResponse({"message": "Failed to create team locally."},status=500)
      else:
        log = Log(code=400, message="Invalid team create payload.", integration=integration)
        log.save()
        return JsonResponse({"message": "Invalid team create payload."},status=400)

    # Update Team
    if payload['team']['type'].lower() == 'update':
      if 'id' in payload['team'] and 'name' in payload['team']:
        try:
          team = Team.objects.get(external_id=payload['team']['id'])
        except:
          log = Log(code=404, message="No team found with external ID.", integration=integration)
          log.save()
          return JsonResponse({"message": "No team found with external ID."}, status=404)
        
        try:
          team.name = payload['team']['name']
          team.save()
          log = Log(code=200, message="Success.", integration=integration)
          log.save()
          return JsonResponse({"message": "Success."},status=200)
        except:
          log = Log(code=500, message="Failed to update team locally.", integration=integration)
          log.save()
          return JsonResponse({"message": "Failed to update team locally."},status=500)
      else:
        log = Log(code=400, message="Invalid team update payload.", integration=integration)
        log.save()
        return JsonResponse({"message": "Invalid team update payload."},status=400)

    # Delete Team
    if payload['team']['type'].lower() == 'delete':
      if 'id' in payload['team']:
        try:
          team = Team.objects.get(external_id=payload['team']['id'])
        except:
          log = Log(code=404, message="No team found with provided ID.", integration=integration)
          log.save()
          return JsonResponse({"message": "No team found with provided ID."},status=404)

        try:
          team.delete()
          log = Log(code=200, message="Success.", integration=integration)
          log.save()
          return JsonResponse({"message": "Success."},status=200)
        except:
          log = Log(code=400, message="Invalid team delete payload.", integration=integration)
          log.save()
          return JsonResponse({"message": "Invalid team delete payload."},status=400)

  # Solve
  elif 'solve' in payload:
    if 'team' not in payload['solve'] or 'challenge' not in payload['solve']:
      log = Log(code=400, message="team or challenge not provided in payload.", integration=integration)
      log.save()
      return JsonResponse({"message": "team or challenge not provided in payload."}, status=400)

    try:
      team = Team.objects.get(external_id=payload['solve']['team'])
    except:
      log = Log(code=404, message="No team exist with that ID.", integration=integration)
      log.save()
      return JsonResponse({"message": "No team exist with that ID."},status=404)

    try:
      challenge = Challenge.objects.get(external_id=payload['solve']['challenge'])
    except:
      log = Log(code=404, message="No challenge exist with that ID.", integration=integration)
      log.save()
      return JsonResponse({"message": "No challenge exist with that ID."}, status=404)

    try:
      node = team.node
    except:
      log = Log(code=500, message="Team is not assigned to a node.", integration=integration)
      log.save()
      return JsonResponse({"message": "Team is not assigned to a node."}, status=500)

    # Check if node or team has this solve.

    # Check if Team has solved this challenge
    try:
      Solve.objects.get(challenge=challenge, team=team)
      log = Log(code=500, message="Team already solved this challenge.", integration=integration)
      log.save()
      return JsonResponse({"message": "Team already solved this challenge."}, status=500)
    except:
      pass

    if node.state:
      if node.state[challenge.balloon]:
        log = Log(code=500, message="Node state for balloon %s is reporting as inactive." % (challenge.balloon), integration=integration)
        log.save()
        return JsonResponse({"message": "Node state for balloon %s is reporting as inactive." % (challenge.balloon)}, status=500)
      else:

        # Send command to AWS
        try:
          broker = Broker.objects.all().first()
        except:
          log = Log(code=500, message="No broker configured.", integration=integration)
          log.save()
          return JsonResponse({"message": "No broker configured."}, status=500)
        
        if not broker:
          log = Log(code=500, message="No broker configured.", integration=integration)
          log.save()
          return JsonResponse({"message": "No broker configured."}, status=500)
        
        publish_url = 'https://%s:%i/topics/hackart/%s?qos=1' % (broker.endpoint, broker.port, node.id)
        new_state = node.state
        new_state[challenge.balloon] = True
        publish_msg = {"type": "pop", "state": new_state}

        publish = requests.request('POST',
          publish_url,
          data=json.dumps(publish_msg),
          cert=['/root/certificate.pem.crt', '/root/private.pem.key'])

        if publish.status_code != 200:
          log = Log(code=500, message="Error with request to AWS.", integration=integration)
          log.save()
          return JsonResponse({"message": "Error with request to AWS."}, status=500)

    else:
      log = Log(code=500, message="Node is in an unknow state. Cannot complete this request.", integration=integration)
      log.save()
      return JsonResponse({"message": "Node is in an unknow state. Cannot complete this request."}, status=500)


    try:
      solve = Solve(challenge=challenge, team=team)
      solve.save()
      log = Log(code=200, message="Success.", integration=integration)
      log.save()
      return JsonResponse({"message": "Success."}, status=200)
    except:
      log = Log(code=500, message="Failed to add solved challenge.", integration=integration)
      log.save()
      return JsonResponse({"message": "Failed to add solved challenge."}, status=500)

      
  # If not team or solve
  else:
    log = Log(code=400, message="Payload is not a Team or Solve object.", integration=integration)
    log.save()
    return JsonResponse({"message": "Payload is not a Team or Solve object."}, status=400)
    
def rom(request):
  key = request.GET.get('key', '')
  player = request.GET.get('player', '')
  balloon = request.GET.get('balloon', '')

  if not key:
    return JsonResponse({"message": "No Key"}, status=401) 
  
  if not player:
    return JsonResponse({"message": "No player passed."}, status=404)
  
  if not balloon:
    return JsonResponse({"message": "No balloon passed."}, status=404) 

  try:
    rom = ROM.objects.get(key=key)
  except:
    return JsonResponse({"message": "No ROM for key."}, status=401) 
  
  if player in ['P1','P2','P3','P4']:
    try:
      p = Player.objects.get(rom=rom, player=player)
    except:
      return JsonResponse({"message": "Could not get player"}, status=500) 
  else:
    return JsonResponse({"message": "Bad player ID."}, status=500) 
  
  state = {'A': False, 'B': False, 'C': False}
  if balloon in ['A', 'B', 'C']:
      state[balloon] = True
  else:
    return JsonResponse({"message": "Bad balloon ID."}, status=500) 

  # Send to AWS
  try:
    broker = Broker.objects.all().first()
  except:
    return JsonResponse({"message": "No broker configured."}, status=500)
  
  if not broker:
    return JsonResponse({"message": "No broker configured."}, status=500)

  publish_url = 'https://%s:%i/topics/hackart/%s?qos=1' % (broker.endpoint, broker.port, p.node.id)
  publish_msg = {"type": "pop", "state": state}

  publish = requests.request('POST',
    publish_url,
    data=json.dumps(publish_msg),
    cert=['/root/certificate.pem.crt', '/root/private.pem.key'])  

  print(publish_url, publish.status_code)
  if publish.status_code == 200:
    return JsonResponse({"message": "Success."}, status=200)
  else:
    return JsonResponse({"message": "General error."}, status=501)