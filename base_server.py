import socket
import threading


class client():
    def __init__(self, server, clientSocket,  onrecieve):
        self.onrecieve = onrecieve
        self.socket = clientSocket
        self.server = server
        self.thread = threading.Thread(target=self.work, args=())
        self.thread.deamon = True
        self.dowork = True

    def send(self, data):
        self.socket.send(data)

    def work(self):
        try:
            while self.dowork:
                data = self.socket.recv(2048)
                if data:
                    self.onrecieve(self, data)
        except Exception :
            self.server.close_client(self)
           


class server(socket.socket):
    def __init__(self, binding, onaccept, onreceive):
        self.should_work = True
        self.onaccept = onaccept
        self.onreceive = onreceive
        self.clients = []
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.bind(binding)
            self.listen(5)
            t = threading.Thread(target=self.work, args=())
            t.deamon = True
        except Exception as e :
            print(e)

    def acceptClient(self, clientsocket):
        c = client(self, clientsocket, self.onreceive)
        self.onaccept(c)
        self.clients.append(c)

    def work(self):
        try:
            while self.should_work:
                clientSocket = self.accept()[0]
                self.acceptClient(clientSocket)
            self.close()
        except Exception as e:
            print(e)
    
    def close_client(self, client):
        self.clients.remove(self)
        client.dowork = False
        client.socket.close()

    def close(self):
        self.should_work = False
        socket.socket.close(self)
