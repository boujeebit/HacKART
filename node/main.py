from umqtt.simple import MQTTClient
import time
import machine
import json
import ubinascii

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
  config_file = open('config.json', 'rb')
except:
  print("No configuration file...")
  led = machine.Pin(16, machine.Pin.OUT)
  led.off()
  time.sleep(10)
  machine.reset()

try:
  config = json.loads(config_file.read())
except:
  print("Unable to load configuration file...")
  led = machine.Pin(16, machine.Pin.OUT)
  led.off()
  time.sleep(10)
  machine.reset()

config_file.close()


if 'mqtt' in config and 'endpoint' in config['mqtt']:
  try:
    if 'certificate' in config['mqtt'] and config['mqtt']['certificate'] and 'key' in config['mqtt'] and config['mqtt']['key']:
      #SSL Enabled
      with open('/certs/'+config['mqtt']['key'], 'rb') as f:
        key_data = f.read()

      with open('/certs/'+config['mqtt']['certificate'], 'rb') as f:
        cert_data = f.read()
          
      SSL_PARAMS = {'key': key_data,'cert': cert_data, 'server_side': False}

      client = mqtt_connect(config['id'], config['mqtt']['endpoint'], ssl=True, ssl_params=SSL_PARAMS)
    else:
      client = mqtt_connect(config['id'], config['mqtt']['endpoint'])
  except OSError as e:
    restart_and_reconnect()

led = machine.Pin(16, machine.Pin.OUT)
led.off()

# Initial Hello
msg = {'MID': ubinascii.hexlify(machine.unique_id()), 'network': station.ifconfig()}
client.publish( topic='testing/test', msg=json.dumps(msg) )

while True:
  try:
    msg= { 'id' : config['id'] }
    client.publish( topic='hackart/heartbeat', msg=json.dumps(msg) )
    # new_message = client.check_msg()
    # if new_message != 'None':
    #   client.publish(topic_pub, b'received')
    time.sleep(60)
  except OSError as e:
    restart_and_reconnect()