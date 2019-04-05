from time import time
from Crypto.Cipher import AES
from Crypto import Random
from protocol import response

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
    token_id = int(token_id)
    expire_time = float(expire_time)
    return token_id == id and expire_time > time()



def pad(to_pad, block_size):
    return to_pad + (block_size - len(to_pad) % block_size) * chr(block_size - len(to_pad) % block_size)


def unpad(to_unpad):
    return to_unpad[:-ord(to_unpad[len(to_unpad)-1:])]


def encrypt(to_encrypt, key):
    raw = pad(to_encrypt, 32)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')


def decrypt(to_decrypt, key):
    enc = base64.b64decode(to_decrypt)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


def require_token(function):
    def wrapper(request, *args, **kwargs):
        if 'ID' not in request['headers'] or 'TOKEN' not in request['headers']:
            return response.unknown_request()
        id = request['headers']['ID']
        token = request['headers']['TOKEN']
        if not check(id,token):
            return response.wrong_authentication()
        return function(request, *args, **kwargs)
    return wrapper