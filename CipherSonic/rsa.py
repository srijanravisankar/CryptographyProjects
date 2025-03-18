import os
import socket
import http.server
import socketserver
from Crypto.PublicKey import RSA

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