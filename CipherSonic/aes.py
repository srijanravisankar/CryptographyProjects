from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import base64

# Function to encrypt data using AES
def encrypt_data(plaintext, key):
    # Ensure the key is 16 bytes (128 bits)
    key = key.ljust(16, b'\0')[:16]
    
    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the plain text to be a multiple of block size
    padded_data = pad(plaintext.encode(), AES.block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    # Return the IV and encrypted data
    return iv + encrypted_data  # Prepend the IV to the encrypted data

# Function to decrypt data using AES
def decrypt_data(encrypted_data, key):
    # Ensure the key is 16 bytes (128 bits)
    key = key.ljust(16, b'\0')[:16]
    
    # Extract the IV (first 16 bytes) from the encrypted data
    iv = encrypted_data[:AES.block_size]
    encrypted_data = encrypted_data[AES.block_size:]

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)

    # Unpad the decrypted data
    return unpad(decrypted_data, AES.block_size).decode()