import aes
import rsa
import audio
import base64

import rsa
import requests

import secrets
import os

key = None

def share_key():
    global key  
    key = secrets.token_bytes(16)

    if not os.path.exists("received_public.pem"):
        print("❌ Error: Public key not received yet. Exchange public keys first!")
        return  

    with open("received_public.pem", "rb") as f:
        public_key_pem = f.read()

    encrypted_key = rsa.encrypt_key(public_key_pem, key)

    with open("encrypted_key.pem", "w") as f:
        f.write(encrypted_key)

    print("🔐 Encrypted AES key saved as encrypted_key.pem")

    print("\n✅ Starting HTTP server to share the encrypted AES key...")
    rsa.start_http_server_key(port=8001)

def get_key():
    global key

    server_url = audio.decode_sound()
    
    if not server_url:
        print("❌ Error: Failed to receive encrypted key URL")
        return

    print(f"🔹 Received encrypted key URL: {server_url}")

    response = requests.get(server_url)

    if response.status_code == 200:
        encrypted_key = response.text.strip()
        print(f"🔐 Retrieved Encrypted AES Key: {encrypted_key}")
    else:
        print("❌ Error: Failed to download the encrypted key")
        return

    with open("private.pem", "rb") as f:
        private_key_pem = f.read()

    try:
        key = rsa.decrypt_key(private_key_pem, encrypted_key)
        print(f"✅ Decrypted AES Key: {key}")
    except Exception as e:
        print(f"❌ Decryption error: {e}")

# encrypt and encode the message into sound waves
def send_message(plaintext):
    global key

    if key is None:
        print("❌ Error: AES key not exchanged yet. Exchange AES keys first!")
        return  

    ciphertext = aes.encrypt_data(plaintext, key)

    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')

    with open("encrypted_message.pem", "w") as f:
        f.write(ciphertext_b64)

    print("🔐 Encrypted message saved as encrypted_message.pem")

    print("\nStarting HTTP server to share the encrypted message...")
    rsa.start_http_server_message(port=8003)

# decode and decrypt the sound waves into message
def receive_message():
    global key

    server_url = audio.decode_sound()

    if not server_url:
        print("❌ Error: Failed to receive encrypted message URL")
        return

    print(f"🔹 Received encrypted message URL: {server_url}")

    response = requests.get(server_url)

    if response.status_code == 200:
        ciphertext_b64 = response.text.strip()
        print(f"🔐 Retrieved Encrypted Message: {ciphertext_b64}")
    else:
        print("❌ Error: Failed to download the encrypted message")
        return

    ciphertext_bytes = base64.b64decode(ciphertext_b64)

    try:
        plaintext = aes.decrypt_data(ciphertext_bytes, key)
        print(f"✅ Decrypted Message: {plaintext}")
        return plaintext
    except Exception as e:
        print(f"❌ Decryption error: {e}")


def main():
    print("Hello from main!")

    while True:
        choice = input("Do you want to send [S] or listen [L] message (or) share [SU] or get [GU] URL (or) share [SK] or get [GK] key?: ")

        if choice == "S":
            message = input("Enter your message: ")
            send_message(message)
        elif choice == "L":
            receive_message()
        elif choice == "SU":
            rsa.share_url()
        elif choice == "GU":
            rsa.get_url()
        elif choice == "SK":
            share_key()
        elif choice == "GK":
            get_key()

if __name__ == "__main__":
    main()