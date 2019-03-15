from base_server import server
import handler


def handle_data(sender,raw_data):
    header, data = str(raw_data).splitlines()
    handler.handle(header,data)



def onreceivedata(sender, data):
    pass

def onaccept(client):
    pass

s = server.server(('', 5050), onaccept, onreceivedata)

while s.shouldWork:
    inp = input('')
    if inp == 'quit':
        s.shouldWork = False
