import time
# from umqtt.simple import MQTTClient
import ubinascii
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

station = network.WLAN(network.STA_IF)
print("\n\n\n")
print("[-] Device details:\n\tHardware ID: %s\n\tMAC Address: %s" % ( ubinascii.hexlify(machine.unique_id()).decode(), ubinascii.hexlify(station.config('mac'),':').decode() ) )

if 'network' in config and 'ssid' in config['network'] and 'password' in config['network']:
  station.active(True)
  station.connect(config['network']['ssid'], config['network']['password'])

  print("[-] Attempting network connection.")
  while station.isconnected() == False:
    pass

  print("[+] Network connection successful.")
  print("[-] Network Details:\n\tIP Address: %s\n\tSubnet Mask: %s\n\tDefault Gateway: %s\n\tDNS: %s" % (station.ifconfig()[0], station.ifconfig()[1], station.ifconfig()[2], station.ifconfig()[3]))
  wifiled = machine.Pin(2, machine.Pin.OUT)
  wifiled.off()

else:
  print("[-] Network object in config file not structured correctly.")
  led = machine.Pin(16, machine.Pin.OUT)
  led.off()
  time.sleep(10)
  machine.reset()