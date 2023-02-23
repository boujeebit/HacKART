


# Certificates

Replace *.*.com with your FQDN.

## Self-signed
For development purposes.

```
openssl req -x509 -newkey rsa:4096 -sha256 -days 365 -nodes \                                                                                                     √ / 10:16:59 
  -keyout server.key -out server.crt -subj "/CN=*.*.com
```


## Let's Encrypt
For production

```
certbot -d *.*.com --manual --preferred-challenges dns certonly
```

# Generate a random key for django
```python
import random
import string

password_characters = string.ascii_letters + string.digits + string.punctuation
''.join(random.choice(password_characters) for i in range(50))
```