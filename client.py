import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('maciej-laptop', 5050))

request = 'TOKEN:|:123456789:-:ROUTE:|:/AUTH/auth:!:body'
s.send(request.encode())
s.close()
