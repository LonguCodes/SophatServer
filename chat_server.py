from base_server import base_server
from protocol import router
from message import data
import json


class chat_server(base_server):

    def __init__(self,binding):
        super().__init__(binding)
        self.connected = []
        self.logged = {}


    def on_accept(self,client):
        print('Client connected : ', client.address)
        self.connected.append(client)
        client.begin_receive()


    def on_receive(self,sender,data):
        request = json.loads(str(data,encoding='UTF-8'))
        response = router.route_request(request)
        print(response)
        sender.begin_send(json.dumps(response).encode())   

    
    def on_disconnect(self,client):
        print('Client disconnected : ', client.address)

    
    def on_loop(self):
        try:
            pass
        except KeyboardInterrupt:
            for chat in data.loaded_chats.keys():
                data.save_chat(chat)
            self.work = False



    




