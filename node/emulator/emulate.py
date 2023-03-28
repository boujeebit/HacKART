import requests, json, datetime

headers = {'key':'11d0fd58-dc97-43da-b96f-55b0461a64a4'}

with open('nodes.json') as file:
    nodes = file.read()

nodes = json.loads(nodes)

while True:
    for node in nodes:
        if node['heartbeat']['last']:
            last = datetime.datetime.fromtimestamp(node['heartbeat']['last']).timestamp()
            if (datetime.datetime.now().timestamp()-last)>node['heartbeat']['interval']:
                print(node['id'], ": Pulse")
                node['heartbeat']['last'] = datetime.datetime.now().timestamp()
                r = requests.post('http://localhost:8000/heartbeat/', headers=headers, json={"id": node['id'], "state": node['state'] })
                print(r)
        else:
            # init
            node['heartbeat']['last'] = datetime.datetime.now().timestamp()

with open('nodes.json', 'w') as file:
    file.write(json.dumps(nodes))


