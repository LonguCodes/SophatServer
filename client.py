import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 5050))

header = 'HEADER:REQUEST'
type = 'AUTHENTICATION'
login = 'admin'
password = 'password'
s.close()
