import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('maciej-laptop', 5050))

request = {
    'headers':{
        'ROUTE':'/AUTH/auth'
    },
    'body':{
        'LOGIN':'sophie',
        'PASS':'sophie123'
    }
}
request_data = json.dumps(request)
s.send(request_data.encode())
print(str(s.recv(2048)))
s.close()
