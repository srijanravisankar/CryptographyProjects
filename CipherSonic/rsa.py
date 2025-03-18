import os
import base64
import socket
import http.server
import socketserver

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from main import send_message, receive_message
from audio import encode_sound, decode_sound

import requests

# Generate RSA keys
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Save private key locally
def save_private_key(private_key, filename="private.pem"):
    with open(filename, "wb") as file:
        file.write(private_key)

# Save public key locally
def save_public_key(public_key, filename="public.pem"):
    with open(filename, "wb") as file:
        file.write(public_key)

# Get local IP address
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Start HTTP server
def start_http_server(port=8000):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving public key at: http://{get_local_ip()}:{port}/public.pem")
        encode_sound(f"http://{get_local_ip()}:{port}/public.pem")
        httpd.handle_request()

def start_http_server_key(port=8001):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving encrypted key at: http://{get_local_ip()}:{port}/encrypted_key.pem")
        encode_sound(f"http://{get_local_ip()}:{port}/encrypted_key.pem")  # Send the link via sound
        httpd.handle_request()  # Serve one request and exit

def share_url():
    # Generate RSA keys
    private_key, public_key = generate_keys()

    # Save private key locally
    save_private_key(private_key, "private.pem")
    print("Private key saved as private.pem")

    # Save public key locally
    save_public_key(public_key, "public.pem")
    print("Public key saved as public.pem")

    # Start HTTP server to share the public key
    print("\nStarting HTTP server...")
    start_http_server()

def get_url():
    # Replace with the correct URL
    server_url = decode_sound()

    if not server_url:
        print("Error: Failed to decode URL into text.")
        return

    # Download the public key
    response = requests.get(server_url)
    if response.status_code == 200:
        public_key = response.content
        with open("received_public.pem", "wb") as file:
            file.write(public_key)
        
        # Load the key for encryption
        rsa_key = RSA.import_key(public_key)
        print("Public key downloaded and ready for encryption!")
    else:
        print("Failed to fetch public key")

def encrypt_key(public_key_pem: bytes, aes_key: bytes) -> str:
    public_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_bytes = cipher.encrypt(aes_key)
    return base64.b64encode(encrypted_bytes).decode()  # Convert to Base64 string

def decrypt_key(private_key_pem: bytes, encrypted_key_b64: str) -> bytes:
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_bytes = base64.b64decode(encrypted_key_b64)
    return cipher.decrypt(encrypted_bytes)  # Decrypt and return the AES key

def start_http_server_message(port=8002):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🔹 Serving encrypted message at: http://{get_local_ip()}:{port}/encrypted_message.pem")
        encode_sound(f"http://{get_local_ip()}:{port}/encrypted_message.pem")  # Send the link via sound
        httpd.handle_request()  # Serve one request and exit
