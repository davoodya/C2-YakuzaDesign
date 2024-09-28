from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import sha256

# generate custom key in 32 chars to use in Fernet
def generate_custom_key(key):
    # Use SHA-256 to get a 32-byte key
    hashed_key = sha256(key.encode()).digest()
    # Encode to Base64 and return
    return urlsafe_b64encode(hashed_key)

# Custom Key init plain text
KEY = "Man Davood Yahay va Mohammad Reza Shams"

# Generate Fernet Key
fernet_key = generate_custom_key(KEY)
cipher = Fernet(fernet_key)

# Encryption
byteText = b"hello my name is Davood Yahay"
encrypted_data = cipher.encrypt(byteText)

# Decryption
decrypted_data = cipher.decrypt(encrypted_data)

# Test Print
print(f"Fernet Key: {fernet_key}")
print(f"Encrypted Data: {encrypted_data}")
print(f"Decrypted Data: {decrypted_data.decode()}")
