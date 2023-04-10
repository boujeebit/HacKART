import os
from dotenv import load_dotenv

load_dotenv()

from identity.models import Broker
from node.models import Node

import requests, json

def publish(id, action, state):
  # print(id, state)

  broker = Broker.objects.all().first()
  if not broker:
    raise Exception("No broker defined.")

  # This might not be needed. Could pass in the node var instead.
  try:
    node = Node.objects.get(id=id)
  except:
    raise Exception("No Node with give ID")

  if action not in ['pop', 'sync']:
    raise Exception("Not a valid action.")
  
  publish_msg = {"type": action, "state": state}
  print("AWS MESSAGE:", publish_msg)

  publish_url = 'https://%s:%i/topics/hackart/%s?qos=1' % (broker.endpoint, broker.port, node.id)
  publish = requests.request('POST',
    publish_url,
    data=json.dumps(publish_msg),
    cert=[os.environ.get('AWS_CRT'), os.environ.get('AWS_KEY')])
  
  if publish.status_code != 200:
    raise Exception("None 200 code from AWS IoT.")
  
  return True