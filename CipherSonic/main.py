import aes
import rsa
import audio
import base64

# encrypt and encode the message into sound waves
def send_message(plaintext):
    # get the message from user
    # plaintext = input("Type your message: ")
    key = b"mysecretkey12345"

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
            send_message()
        elif choice == "L":
            receive_message()
        elif choice == "SU":
            rsa.share_url()
        elif choice == "GU":
            rsa.get_url()

if __name__ == "__main__":
    main()