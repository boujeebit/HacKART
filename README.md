# HacKART

> **Warning** 
>
>**Users of this software assume all liability**. Code in this repository enables hardware to pop balloons in a manor that could cause physical or enviromental harm. The author and its contributors are not responsible for any damages as a result. 

HacKART is a Mario Kart inspired CTF hacking challenge where NodeMCUs are used to pop balloons when a challenge is sovled. The NodeMCU client is written using MicroPython firmware on a NodeMCU with a ESP8266 chipset and 1MB of memory. In future iterations testing will also be done on ESP32 chipset.

Since the NodeMCU's are flashed with MicroPython firmware the client is written in Python. The client uses MQTT messages for its command and control path making it very lightweight. The client supports both AWS IoT and Mosquitto as brokers. If you use AWS IoT (recommended) you will need a certificate for authentication. It is extremely import those certificates are in binary format (more on this later in the setup guide). The NodeMCU will both subscribe and publish to topics. 

## Client Setup

To setup the client all you need is a config file loaded onto the root of the NodeMCU. On boot the NodeMCU will load the config file and begin connecting.

### Client Configuration

A example configuration file is below:

```json
{
    "id": "random-genorated-nodeid",
    "network": {
        "ssid": "your-ssid-here",
        "password": "your-wireless-password-here"
    },
    "heartbeat" : {
        "enabled": true,
        "interval": 5
    },
    "mqtt": {
        "endpoint": "broker-endpoint",
        "certificate": "certificate.der.crt",
        "key": "private.der.key"
    }
}
```

### Client Heartbeat

If you enable client heartbeats the control server will get messages from the NodeMCU so it knows it is still online. Currently, the message is limited to just the Nodes ID.

```json
{
    "id": "nodeid"
}
```