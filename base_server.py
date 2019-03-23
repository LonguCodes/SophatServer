import socket
import threading
from queue import Queue

BUFFER_SIZE = 2048


class client():
    def __init__(self, server, socket, address):
        self.socket = socket
        self.address = address
        self.server = server
        self.socket.settimeout(2)
        self.tasks = Queue()
        self.try_receive = False
        self.work = True
        self.thread = threading.Thread(
            target=self.threader, daemon=True, args=())
        self.thread.start()
        
    def begin_receive(self, callback):
        print('Starting to receive')
        self.try_receive = True
        self.tasks.put((self.task_receive, (callback,)))

    def end_receive(self):
        self.try_receive = False

    def begin_send(self, data, callback):
        self.tasks.put((self.task_send, (data, callback)))

    def task_receive(self, callback):
        data = ''.encode()
        try:
            # Try to get data as long as the other side is sending
            while True:
                data_part = None
                # Try to get data
                # If threre is an exception, the client is not sending data anymore
                try:
                    data_part = self.socket.recv(BUFFER_SIZE)
                    data += data_part
                except: 
                    pass
                # If there is no data, stop receiving
                if len(data_part) < BUFFER_SIZE:
                    break
            
            # If there was anyting send, call the callback and stop trying to recieve
            if len(data) > 0:
                try:
                    callback(self, data)
                except Exception as e:
                    if self.server.debug:
                        print(repr(e))
                self.try_receive = False
            # If not, if there should recieve, start loop back
            elif self.try_receive:
                self.tasks.put((self.task_receive, (callback,)))
        except:
            # The conncetion was lost, remove the client from clients list
            self.close()

    def task_send(self, data, callback=None):
        # Send all the data
        try:
            sent = 0
            while sent < len(data):
                sent += self.socket.send(data[sent:sent+BUFFER_SIZE])
            # If the sending was complete, call th callback
            if callback:
                callback(self)
        except:
            # The conncetion was lost, remove the client from clients list
            self.close()



    def threader(self):
        try:
            while self.work:
                if self.tasks.empty():
                    continue
                
                task = self.tasks.get()
                task[0](*task[1])
        except Exception as e:
            if self.server.debug:
                print(e)

    def close(self):
        self.socket.close()
        self.work = False
        self.server.clients.remove(self)


class server(socket.socket):
    def __init__(self, binding, on_accept = None):
        self.work = True
        self.on_accept = on_accept
        self.clients = []
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        try:
            #Try to set up the server
            self.bind(binding)
            self.listen(5)
            self.settimeout(5)
            # Set up the thread for the server 
            t = threading.Thread(target=self.threader, args=())
            t.start()
        except Exception as e:
            # There was a problem with initializing the server
            print(e)


    def acceptClient(self, socket,address):
        c = client(self, socket, address)
        if self.on_accept:
            self.on_accept(c)
        self.clients.append(c)

    def threader(self):
        while self.work:
            try:
                self.acceptClient(*self.accept())
            except:
                pass
        for client in self.clients:
            client.close()
        self.close()
