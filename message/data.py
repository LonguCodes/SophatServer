import os
import settings
from time import time
import json

MESSAGE_SIZE = 4

loaded_chats = {
    
}

# Get the path to the file that contains messages in the chat
def message_path(chat_id):
    return os.path.join(settings.MESSAGE_PATH, str(chat_id))+'.msg'


# Get the path to the file that contains information about the chat
# For example the users, indexer etc
def data_path(chat_id):
    return os.path.join(settings.CHAT_PATH, str(chat_id))+'.cht'    



def add_new_message(chat_id,sender,content):

    if chat_id not in loaded_chats:
        load_chat(chat_id)        

    message = {
            'id':loaded_chats[chat_id]['data']['indexer'],
            'sender':sender,
            'timestamp':time(),
            'content':content
        }
    loaded_chats[chat_id]['data']['indexer']+= 1
    loaded_chats[chat_id]['messages'].append(message)
    return message

def create_new_chat(chat_id,users):
    loaded_chats[chat_id] = {
            'data':{
                'indexer':0,
                'users':users
            },
            'messages':[],
            
        }

def load_data(chat_id):
    with open(data_path(chat_id),'r') as file:
        loaded_chats[chat_id]['data'] =  json.load(file) 


def load_messages(chat_id):
    path_messages = message_path(chat_id)
    path_data = data_path(chat_id)
    if not os.path.exists(path_messages) or not os.path.exists(path_data):
        return None
    if chat_id not in loaded_chats:
        load_data(chat_id)
    for message in read_message(path_messages):
        loaded_chats[chat_id]['messages'].insert(0,message)
        yield message

def load_chat(chat_id, message_count = 0):
    loaded_chats[chat_id] = {
        'data':{},
        'messages':[]
    }
    load_data(chat_id)
    messages = load_messages(chat_id)
    for i in range(message_count):
        try:
            next(messages)
        except:
            pass
        


def read_message(file_path):
    with open(file_path, 'rb') as file:
        file.seek(0, 2)
        remaining = file.tell()
        while remaining > 0:
            file.seek(-MESSAGE_SIZE, 1)
            size = int.from_bytes(file.read(MESSAGE_SIZE), byteorder='little')
            file.seek(-size-MESSAGE_SIZE, 1)
            remaining -= size+MESSAGE_SIZE
            decoded = file.read(size).decode('utf-8')
            message = json.loads(decoded)
            file.seek(-size, 1)
            yield message


def save_chat(chat_id):
    save_data(chat_id)
    save_messages(chat_id)

def save_data(chat_id):
    path = data_path(chat_id)

    if not os.path.isdir(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))

    with open(path,'w') as file:
        json.dump(loaded_chats[chat_id]['data'],file) 

def save_messages(chat_id):
    file_chat = load_messages(chat_id)
    try:
        last_id = next(file_chat)['id'] + 1
    except StopIteration:
        last_id = 0

    path = message_path(chat_id)
    if not os.path.isdir(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    if not os.path.exists(path):
        open(path, 'x').close()

    chat = loaded_chats[chat_id]['messages']

    with open(path, 'ab') as file:
        for message in chat[last_id:]:
            serialized = json.dumps(message)
            bytes_to_write = serialized.encode('utf-8')
            file.write(bytes_to_write)
            count = len(bytes_to_write)
            byte_count = count.to_bytes(MESSAGE_SIZE, byteorder='little')
            file.write(byte_count)