import datetime

def try_auth(client, data):
    
    try:
        login,password = data.split()    
        id = 0
        token = generate_token(id)
        client.send(bytes(token))
    except Exception:
        print('Authentication error')
        client.close()

def generate_token(id):
    return str(id) + str(datetime.datetime.now())
