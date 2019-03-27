import os
import settings
from datetime import datetime
import json

MESSAGE_SIZE = 32

def sanitize_message(message):
    return message.replace('\n','\\n')

def desanitize_message(message):
    return message.replace('\\n','\n')

def chat_path(chat_id):
    return f'{settings.MESSAGE_PATH}{chat_id}.msg'

def save_chat(chat_id,chat):
    last = next(load_chat(chat_id))
    with open(chat_path(chat_id),'a') as file:
        for message in chat[last['id']+1:]:
            serialized = json.dumps(message)
            file.write()
            
        

def load_chat(chat_id):
    for message in read_chat(chat_path(chat_id)):
        yield message   
        
def read_chat(file_path):
    with open(file_path) as file:
        file.seek(2,0)
        remaining = file.tell()
        while remaining > 0:
            file.seek(1,-MESSAGE_SIZE)
            size = int(file.read(MESSAGE_SIZE)) 
            file.seek(1,-size-MESSAGE_SIZE)
            remaining -= size+MESSAGE_SIZE
            yield json.loads(file.read(size))
            file.seek(1,-size)
                        

def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # The first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # If the previous chunk starts right from the beginning of line
                # do not concat the segment to the last line of new chunk.
                # Instead, yield the segment first
                if buffer[-1] != '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment
