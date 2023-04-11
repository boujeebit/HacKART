from umqtt.simple import MQTTClient
import os, machine, sys, ubinascii
import time, json

if boot_failure is True:
  sys.exit()

# Init the default state and heartbeat
state = {'A': False, 'B': False, 'C': False}
heartbeat = 0

r1 = machine.Pin(12, machine.Pin.OUT) #A
r2 = machine.Pin(13, machine.Pin.OUT) #B
r3 = machine.Pin(15, machine.Pin.OUT) #C

# Function to validate local state and MQTT state messages.
def validate_state(state):
  if 'A' in state and 'B' in state and 'C' in state:
    if type(state['A']) is bool and type(state['B']) is bool and type(state['C']) is bool:
      return True
  return False

# MQTT Callback function
def sub_cb(topic, msg):
  global state
  global heartbeat

  print("[+] Message recieved from topic: ", topic)
  try:
    msg = json.loads(msg)
  except:
    print(" ↳ [!] Bad message from C2, not json.")
    return

  if 'type' not in msg or msg['type'] not in ['pop', 'sync']:
    print(" ↳ [!] Invalid Type")
    return

  if 'state' not in msg or not validate_state(msg['state']):
    print(" ↳ [!] Invalid state in message.")
    return

  if msg['type'] == 'pop':
    for x in msg['state']:
      if msg['state'][x] is True and msg['state'][x] != state[x]:
        if x == 'A':
          r1.value(1)
          time.sleep(1)
          r1.value(0)
        if x == 'B':
          r2.value(1)
          time.sleep(1)
          r2.value(0)
        if x == 'C':
          r3.value(1)
          time.sleep(1)
          r3.value(0)

        print(" ↳ Popping:", x)

  elif msg['type'] == 'sync':
    print(" ↳ Sync requested. New state: ", msg['state'])
    for x in msg['state']:
      if msg['state'][x] is False:
        if x == 'A':
          r1.value(0)
        if x == 'B':
          r2.value(0)
        if x == 'C':
          r3.value(0)

  # Writing new state to local state file.
  with open('state.json', 'w') as f: 
    f.write(json.dumps(msg['state']))

  state = msg['state']
  heartbeat = 0

  return

def mqtt_connect(clientID, endpoint, port=8883, keepalive=10000, ssl=False, ssl_params=None):
  print(" ↳ Endpoint: %s:%i" % (endpoint, port))
  client = MQTTClient(clientID, endpoint, port=port, keepalive=keepalive, ssl=ssl, ssl_params=ssl_params)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe('hackart/'+clientID)

  return client

# Read in Certificate data.
try:
  with open('/certs/'+config['mqtt']['ssl']['certificate'], 'rb') as f:
    cert_data = f.read()
except OSError:
  print("[!] Certificate was not loaded properly. Ensure DER formatting." )
  sys.exit()

# Read in Private key data.
try:
  with open('/certs/'+config['mqtt']['ssl']['key'], 'rb') as f:
    key_data = f.read()
except OSError:
  print("[!] Private key was not loaded properly. Ensure DER formatting." )
  sys.exit()

# Init State as default for from file.
if 'state.json' in os.listdir():
  local_state = {}
  with open("state.json", 'r') as state_file:
    try:
      local_state = json.loads(state_file.read())
    except KeyboardInterrupt:
      raise
    except Exception as error:
      print("[!] Unable to read 'state.json' file.")
    
  if local_state and validate_state(local_state):
    print("[+] Using state from local file: ", local_state)
    state = local_state
  else:
    print("[+] State is set to DEFAULT.")
else:
    print("[+] State is set to DEFAULT.")

# Attempt MQTT Connection
print("[-] Attempting to connect to MQTT broker over ssl.")
try:
  client = mqtt_connect(config['id'], config['mqtt']['endpoint'], ssl=True, ssl_params={'key': key_data,'cert': cert_data, 'server_side': False})
  print("[+] MQTT connection made successfully.")
except KeyboardInterrupt:
  raise
except Exception as error:
  print("[!] Unable to establish a MQTT connection")
  sys.exit()

# Initial Hello
print("[-] Sending startup heartbeat.")
msg = {'id': config['id'], 'state': state, 'initialized': { 'mid': ubinascii.hexlify(machine.unique_id()), 'interface': { 'ssid': config['network']['ssid'], 'mac': ubinascii.hexlify(station.config('mac'),':').decode(), 'lease': station.ifconfig() }, 'heartbeat': { 'enabled': config['heartbeat']['enabled'], 'interval': config['heartbeat']['interval'] } } }
client.publish( topic='hackart/heartbeat', msg=json.dumps(msg) )
print("[+] Startup heartbeat sent.")

# Start main listening loop.
print("\n\n[+] Starting normal operations..\n")

if config['heartbeat']['enabled']:
  heartbeat = time.ticks_add(time.ticks_ms(), config['heartbeat']['interval']*1000)
else:
  heartbeat = 0

while True:
  if config['heartbeat']['enabled'] and time.ticks_diff(heartbeat, time.ticks_ms()) < 0:
    client.publish( topic='hackart/heartbeat', msg=json.dumps({'id' : config['id'], 'state': state}) )
    print("[+] Heartbeart: ", state)
    heartbeat = time.ticks_add(time.ticks_ms(), config['heartbeat']['interval']*1000)

  try:
    client.check_msg()
  except OSError as e:
    machine.reset()