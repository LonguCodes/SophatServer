from time import time
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib

EXPIRY_TIME = 600

def generate(id):
    # TODO : Make a sql quary to get the key for the encryption
    key = 'abcabc'
    encryption_key = hashlib.sha256(key.encode()).digest()
    to_encrypt = f'{id}:{str(time()+EXPIRY_TIME)}'
    return encrypt(to_encrypt, encryption_key)


def check(id, token):
    # TODO : Make a sql quary to get the key for the encryption
    key = 'abcabc'
    encryption_key = hashlib.sha256(key.encode()).digest()
    decrypted = decrypt(token, encryption_key)
    token_id, expire_time = decrypted.split(':')
    return token_id == id and expire_time > time()



def pad(to_pad, block_size):
    return to_pad + (block_size - len(to_pad) % block_size) * chr(block_size - len(to_pad) % block_size)


def unpad(to_unpad):
    return to_unpad[:-ord(to_unpad[len(to_unpad)-1:])]


def encrypt(to_encrypt, key):
    raw = pad(to_encrypt, 32)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(to_decrypt, key):
    enc = base64.b64decode(to_decrypt)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


def require_token(function):
    def wrapper(*args, **kwargs):
        request = args[0]
        if 'ID' not in request['headers'] or 'TOKEN' not in request['headers']:
            return {
                'headers':{
                    'response' : 2,
                }
            }
        id = request['headers']['ID']
        token = request['headers']['TOKEN']
        if not check(id,token):
            return {
                'headers':{
                    'response' : 2,
                }
            }
        return function(*args, **kwargs)
    return function