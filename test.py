import socket

s = socket.socket()
s.bind(('',10101))
s.listen(5)
client, add = s.accept()
client.recv(2048)
client.send('test'.encode())

client.close()

s.close()