import os
from datetime import datetime

print(datetime.utcnow().second)

BASE_PATH = os.path.dirname(os.path.realpath(__file__)) 

MESSAGE_DIR = '/messages/'
MESSAGE_PATH = f'{BASE_PATH}{MESSAGE_DIR}'
