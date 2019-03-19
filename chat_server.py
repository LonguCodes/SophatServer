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
    request = parse_request(data)
    router.route(request)



def onreceivedata(sender, data):
    handle_data(sender,data)
    pass

def onaccept(client):
    pass


s = server(('', 5080), onaccept, onreceivedata)

try:
    while s.should_work:
        pass
except KeyboardInterrupt:
    s.shut_server()
    print('\n')

