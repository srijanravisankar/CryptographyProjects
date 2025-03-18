import aes
import rsa
import audio
import base64

import rsa
import requests

key = b"mysecretkey12345"

def share_key():
    global key  # AES key for encryption

    # Load public key
    with open("received_public.pem", "rb") as f:
        public_key_pem = f.read()

    # Encrypt AES key using RSA public key
    encrypted_key = rsa.encrypt_key(public_key_pem, key)

    # Save encrypted AES key to a file for HTTP sharing
    with open("encrypted_key.pem", "w") as f:
        f.write(encrypted_key)

    print("Encrypted AES key saved as encrypted_key.pem")

    # Start HTTP server
    print("\nStarting HTTP server to share the encrypted key...")
    rsa.start_http_server_key(port=8001)  # Serve encrypted_key.pem

def get_key():
    global key

    # Receive the URL via sound
    server_url = audio.decode_sound()
    
    if not server_url:
        print("❌ Error: Failed to receive encrypted key URL")
        return

    print(f"🔹 Received encrypted key URL: {server_url}")

    # Fetch the encrypted AES key from the server
    response = requests.get(server_url)

    if response.status_code == 200:
        encrypted_key = response.text.strip()
        print(f"🔐 Retrieved Encrypted AES Key: {encrypted_key}")
    else:
        print("❌ Error: Failed to download the encrypted key")
        return

    # Load private key
    with open("private.pem", "rb") as f:
        private_key_pem = f.read()

    # Decrypt the AES key
    try:
        key = rsa.decrypt_key(private_key_pem, encrypted_key)
        print(f"✅ Decrypted AES Key: {key.decode()}")
    except Exception as e:
        print(f"❌ Decryption error: {e}")


# encrypt and encode the message into sound waves
def send_message(plaintext):
    global key

    # encrypt the message
    ciphertext = aes.encrypt_data(plaintext, key)
    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')

    # encode and output the sound
    audio.encode_sound(ciphertext_b64)

# decode and decrypt the sound waves into message
def receive_message():
    # listen and decode the sound
    ciphertext_b64 = audio.decode_sound()
    key = b"mysecretkey12345"

    if not ciphertext_b64:
        print("Error: Failed to decode sound into text.")
        return

    # ensure correct Base64 decoding
    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)  # Correct Base64 decoding
    except Exception as e:
        print(f"Base64 decoding error: {e}")
        return

    # decrypt and output the message
    try:
        plaintext = aes.decrypt_data(ciphertext_bytes, key)
        print("Decrypted Message:", plaintext)
        return plaintext
    except Exception as e:
        print(f"Decryption error: {e}")

def main():
    print("Hello from main!")

    while True:
        # ask if the user want to send or listen
        choice = input("Do you want to send [S] or listen [L] message (or) share [SU] or get [GU] URL (or) share [SK] or get [GK] key?: ")

        # call the function according to the user choice
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