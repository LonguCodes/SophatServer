import os
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) 

DATA_DIR = 'data'
DATA_PATH = os.path.join(BASE_PATH,DATA_DIR)

CHAT_DIR = 'chats'
CHAT_PATH = os.path.join(DATA_PATH,CHAT_DIR)


MESSAGE_DIR = 'messages'
MESSAGE_PATH = os.path.join(DATA_PATH,MESSAGE_DIR)
