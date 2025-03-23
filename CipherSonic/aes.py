from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import base64

# Function to encrypt data using AES
def encrypt_data(plaintext, key):
    print(f"Encrypting text '{plaintext}' ...")
    key = key.ljust(16, b'\0')[:16]
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return iv + encrypted_data

# Function to decrypt data using AES
def decrypt_data(encrypted_data, key):
    key = key.ljust(16, b'\0')[:16]
    iv = encrypted_data[:AES.block_size]
    encrypted_data = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_data, AES.block_size).decode()