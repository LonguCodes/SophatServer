from base_server import server
import router

def parse_request(data):
    header, body = data.split(':!:')
    headers = dict([tuple(h.split(':|:')) for h in header.split(':-:')])
    
    return {
        'headers': headers,
        'body' : body
    }

def handle_data(sender,data):
    request = parse_request(str(data))
    router.route(request)


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

