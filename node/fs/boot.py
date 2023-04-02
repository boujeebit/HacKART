import os, esp, gc, sys, ubinascii, machine, network, json

esp.osdebug(None)
gc.collect()

version = "1.1"
# Padding for REPL restart
print("\n\n")

def validate_config(config):
  if 'id' not in config or 'network' not in config or 'mqtt' not in config or 'heartbeat' not in config:
    return False
  if 'ssid' not in config['network'] or 'password' not in config['network']:
    return False
  if 'endpoint' not in config['mqtt'] or 'ssl' not in config['mqtt']:
    return False
  if 'certificate' not in config['mqtt']['ssl'] or 'key' not in config['mqtt']['ssl']:
    return False
  if 'enabled' not in config['heartbeat']:
    return False
    
  return True

try:
  os.stat('config.json')
except OSError:
  print("[!] No 'config.json' file on board.")
  sys.exit()

with open("config.json", 'r') as config_file:
  try:
    config = json.loads(config_file.read())
  except KeyboardInterrupt:
    raise
  except Exception as error:
    print("[!] Unable to read 'config.json' file.")
    sys.exit()

if not validate_config(config):
  print("[!] Configuration file is not properly formated.")
  sys.exit()

# Ensure Certificates are on filesystem
try:
  os.stat('certs/'+config['mqtt']['ssl']['certificate'])
except OSError:
  print("[!] Certificate '%s' was not found in the cert/ directory." % ( config['mqtt']['ssl']['certificate'] ) )
  sys.exit()

try:
  os.stat('certs/'+config['mqtt']['ssl']['key'])
except OSError:
  print("[!] Private key '%s' was not found in the cert/ directory." % ( config['mqtt']['ssl']['certificate'] ) )
  sys.exit()

# Init station
station = network.WLAN(network.STA_IF)

# Device details
print("[-] Device details:\n ↳ Code Version: %s\n ↳ HacKART ID: %s\n ↳ Hardware ID: %s\n ↳ MAC Address: %s" % ( version, config['id'], ubinascii.hexlify(machine.unique_id()).decode(), ubinascii.hexlify(station.config('mac'),':').decode() ) )

# Attempt network connection
station.active(True)
station.connect(config['network']['ssid'], config['network']['password'])

print("[-] Attempting network connection.\n ↳ SSID: %s" % (config['network']['ssid']))
while station.isconnected() == False:
  pass

print("[+] Network connection successful.")
print("[-] Network Details:\n ↳ IP Address: %s\n ↳ Subnet Mask: %s\n ↳ Default Gateway: %s\n ↳ DNS: %s" % (station.ifconfig()[0], station.ifconfig()[1], station.ifconfig()[2], station.ifconfig()[3]))

# Turn on station LED
wifiled = machine.Pin(2, machine.Pin.OUT)
wifiled.off()