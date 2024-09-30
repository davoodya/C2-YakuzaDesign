from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from settings import KEY


def pad_key(key):
    """this function will statisfy encryption Key requirements to having a full 32 characters"""
     # While key length is not 32 characters, add P to the end of the key until it is 32 chars
    while len(key) % 32 != 0:
        key += "P"
    return key


"""Pad out key to 32 chars, then byte encoding and urlsafe_b64 encoding do on key, 
then create a AES/CBC mode Cipher Object"""
cipher = Fernet(urlsafe_b64encode(pad_key(KEY).encode()))
