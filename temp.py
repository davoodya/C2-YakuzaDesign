from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

# Way 1: Create Random key
# key = Fernet.generate_key()

# Way 2: Create Customized key
KEY = "U can't touch this!"

def pad_key(key):
    """this function will statisfy encryption Key requirements to having a full 32 characters"""
     # While key length is not 32 characters, add P to the end of the key until it is 32 chars
    while len(key) % 32 != 0:
        key += "P"
    return key

"""Pad out key to 32 chars, then byte encoding and urlsafe_b64 encoding do on key, 
then create a AES/CBC mode Cipher Object"""

# padded_key = pad_key(KEY)
# encoded_key = urlsafe_b64encode(padded_key.encode())

cipher = Fernet(urlsafe_b64encode(pad_key(KEY).encode()))

# Encryption
token = cipher.encrypt(b"This is Dark Deep Secret")
# Decryption
decryptedToken = cipher.decrypt(token)

# Test Print
print(f"Encrypted Data Type: " ,type(token))
print(f"Encrypted Data: " , token)
print(f"---------------------------\n")
print(f"Customized Key: " , urlsafe_b64encode(pad_key(KEY).encode()))
print(f"Decrypted Data: " , decryptedToken)
