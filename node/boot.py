import time
# from umqtt.simple import MQTTClient
# import ubinascii
import machine
import network
import json
import esp
esp.osdebug(None)
import gc
gc.collect()

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

if 'network' in config and 'ssid' in config['network'] and 'password' in config['network']:
  station = network.WLAN(network.STA_IF)

  station.active(True)
  station.connect(config['network']['ssid'], config['network']['password'])

  while station.isconnected() == False:
    pass

  print('Connection successful')
  print(station.ifconfig())
  wifiled = machine.Pin(2, machine.Pin.OUT)
  wifiled.off()

else:
  print("Network object in config file not strcuted correctly...")
  led = machine.Pin(16, machine.Pin.OUT)
  led.off()
  time.sleep(10)
  machine.reset()