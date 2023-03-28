from umqtt.simple import MQTTClient
import time
import machine
import json
import ubinascii

def critical_failure():
  led = machine.Pin(16, machine.Pin.OUT)
  while True:
    led.off()
    time.sleep(0.2)
    led.on()
    time.sleep(0.2)

def flash_red():
  led = machine.Pin(16, machine.Pin.OUT)
  for x in range(10):
    led.off()
    time.sleep(0.2)
    led.on()
    time.sleep(0.2)

def sub_cb(topic, msg):
  print((topic, msg))

def mqtt_connect(clientID, endpoint, port=8883, keepalive=10000, ssl=False, ssl_params=None):
  client = MQTTClient(clientID, endpoint, port=port, keepalive=keepalive, ssl=ssl, ssl_params=ssl_params)
  # client.set_callback(sub_cb)
  client.connect()
  # client.subscribe(topic_sub)
  # print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  flash_red()
  time.sleep(10)
  machine.reset()


try:
  print("[+] Loading configuration file.")
  config_file = open('config.json', 'rb')
  config = json.loads(config_file.read())
except:
  print("[-] Failed to load the configuration.")
  critical_failure()

print("[+] Configuration file loaded successfully.")
config_file.close()


if 'mqtt' in config and 'endpoint' in config['mqtt']:
  try:
    if 'ssl' in config['mqtt'] and 'certificate' in config['mqtt']['ssl'] and config['mqtt']['ssl']['certificate'] and 'key' in config['mqtt']['ssl'] and config['mqtt']['ssl']['key']:
      #SSL Enabled
      print("[-] SSL enabled MQTT identitied in configuation.")
      with open('/certs/'+config['mqtt']['ssl']['key'], 'rb') as f:
        key_data = f.read()

      with open('/certs/'+config['mqtt']['ssl']['certificate'], 'rb') as f:
        cert_data = f.read()
          
      SSL_PARAMS = {'key': key_data,'cert': cert_data, 'server_side': False}

      print("[-] Attempting to connect to MQTT broker over ssl.")
      client = mqtt_connect(config['id'], config['mqtt']['endpoint'], ssl=True, ssl_params=SSL_PARAMS)
      print("[+] MQTT connection made successfully.")
    else:
      print("[-] Malformed SSL settings in the configuration file.")
      critical_failure()
  except OSError as e:
    restart_and_reconnect()
else:
  print("[!] No MQTT/Endpoint setting in configuration file.")
  critical_failure()

led = machine.Pin(16, machine.Pin.OUT)
led.off()

# Load state
try:
  print("[+] Loading state file")
  state_file = open('config.json', 'rb')
  state = json.loads(state_file.read())
  if 'A' in state and 'B' in state and 'C' in state:
    if type(state['A']) is bool and type(state['B']) is bool and type(state['C']) is bool:
      print("[+] State file loaded.")
    else:
      print("[-] Malformed state data. Starting fresh..")
      state = {"A": False, "B": False, "C": False}
except:
  print("[-] Failed to load state file. Starting fresh..")
  state = {"A": False, "B": False, "C": False}



# Initial Hello
print("[-] Sending startup heartbeat.")
msg = {'id': config['id'], 'state': state, 'initialized': { 'mid': ubinascii.hexlify(machine.unique_id()), 'interface': { 'mac': '', 'lease': station.ifconfig() }, 'heartbeat': { 'enabled': True, 'interval': 60 } } }
client.publish( topic='hackart/heartbeat', msg=json.dumps(msg) )
print("[+] Startup heartbeat sent.")




print("\n\n[+] Starting normal operations..\n")
while True:
  try:
    msg= { 'id' : config['id'], 'state': state }
    # client.publish( topic='hackart/heartbeat', msg=json.dumps(msg) )
    print(msg)
    # new_message = client.check_msg()
    # if new_message != 'None':
    #   client.publish(topic_pub, b'received')
    time.sleep(60)
  except OSError as e:
    restart_and_reconnect()