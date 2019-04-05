import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('maciej-laptop', 5062))

request = {
    'headers':{
        'ROUTE':'/AUTH/auth'
    },
    'body':{
        'LOGIN':'sophie',
        'PASSWORD':'sophie123'
    }
}
request_data = json.dumps(request)
s.send(request_data.encode())
response = json.loads(s.recv(2048).decode('utf-8'))
print(response)


token = response['body']['TOKEN']

user_id = response['body']['ID']


request_v2 = {
    'headers':{
        'ROUTE':'/MESSAGE/send',
        'TOKEN':token,
        'ID':user_id
    },
    'body':{
        'CHAT_ID':0,
        'SENDER':user_id,
        'CONTENT':"test"
        
    }
}

s.send(json.dumps(request_v2).encode())

response_v2 = json.loads(s.recv(2048).decode('utf-8'))

print(response_v2)

s.close()
