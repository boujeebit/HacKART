# Node Setup Guide


## Config example:

```json
{
    "id": "random-genorated-nodeid",
    "network": {
        "ssid": "your-ssid-here",
        "password": "your-wireless-password-here"
    },
    "heartbeat" : {
        "enabled": true,
        "interval": 60,
        "topic": "hackart/heartbeat"
    },
    "mqtt": {
        "endpoint": "broker-endpoint",
        "port": 8883,
        "keepalive": 10000,
        "ssl" : {
            "certificate": "certificate.der.crt",
            "key": "private.der.key"
        }
    }
}
```

## Heartbeats

### Initial Heartbeat

```json
{
  "id": "node_id",
  "initialized": {
    "mid": "machine_id",
    "interface": {
      "mac": "mac address",
      "lease": [
        "ip address",
        "subnet mask",
        "default gateway",
        "dns"
      ]
    },
    "heartbeat": {
      "enabled": true,
      "topic": "hackart/heartbeat",
      "interval": 60
    }
  }
}
```