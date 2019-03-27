from base_server import server
from protocol import router
import json


def handle_data(sender,data):
    request = json.loads(str(data,encoding='UTF-8'))
    response = router.route_request(request)
    sender.begin_send(json.dumps(response).encode(), lambda s : s.begin_receive(handle_data))    
        


def on_accept(client):
    print('Accepted client : ', client.address)
    client.begin_receive(handle_data)
    pass

s = server(('0.0.0.0', 5050), on_accept)
s.debug = True
print('Server started')
try:
    while s.work:
        pass
except KeyboardInterrupt:
    print('Stopping server')
    s.work = False

