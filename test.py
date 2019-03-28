from message import data



chat = [
    {
        'id':0,
        'sender':0,
        'timestamp':1,
        'message':'test message { }'

    }
]
# data.save_chat(0,chat)
for message in data.load_chat(0):
   print(message)
