import os
import settings
from datetime import datetime
import json

MESSAGE_SIZE = 32


def chat_path(chat_id):
    return os.path.join(settings.MESSAGE_PATH, str(chat_id))+'.msg'


def save_chat(chat_id, chat):
    file_chat = load_chat(chat_id)
    try:
        last_id = next(file_chat)['id'] + 1
    except StopIteration:
        last_id = 0

    path = chat_path(chat_id)
    if not os.path.isdir(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    if not os.path.exists(path):
        open(path, 'x').close()

    with open(path, 'ab') as file:
        for message in chat[last_id:]:
            serialized = json.dumps(message)
            bytes_to_write = serialized.encode('utf-8')
            file.write(bytes_to_write)
            count = len(bytes_to_write)
            byte_count = count.to_bytes(32, byteorder='little')
            file.write(byte_count)


def load_chat(chat_id):
    path = chat_path(chat_id)
    if not os.path.exists(path):
        return []
    for message in read_chat(path):
        yield message


def read_chat(file_path):
    with open(file_path, 'rb') as file:
        file.seek(0, 2)
        remaining = file.tell()
        while remaining > 0:
            file.seek(-MESSAGE_SIZE, 1)
            size = int.from_bytes(file.read(MESSAGE_SIZE), byteorder='little')
            file.seek(-size-MESSAGE_SIZE, 1)
            remaining -= size+MESSAGE_SIZE
            message = json.loads(file.read(size).decode('utf-8'))
            file.seek(-size, 1)
            yield message