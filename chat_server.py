from base_server import server
import router
import json


def handle_data(sender,data):
    request = json.loads(str(data,encoding='UTF-8'))
    response = router.route_request(request)
    print(json.dumps(response)) 
    sender.begin_send(json.dumps(response).encode())    
    


def on_accept(client):
    print('Accepted client : ', client.address)
    client.begin_receive(handle_data)
    pass

print('Starting server')
s = server(('0.0.0.0', 5050), on_accept)
s.debug = True
print('Server started')
try:
    while s.work:
        pass
except KeyboardInterrupt:
    print('Stopping server')
    s.work = False

