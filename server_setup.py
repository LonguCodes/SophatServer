import sys
import socket

arg = sys.argv[1]

if arg == 'ip':
    print(socket.gethostname())