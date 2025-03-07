import aes
import audio

import base64

# encrypt and encode the message into sound waves
def send_message():
    print("Hello from play sound!")

    # get the message from user
    plaintext = input("Type your message: ")
    key = b"mysecretkey12345"

    # encrypt the message
    ciphertext = aes.encrypt_data(plaintext, key)
    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')

    print(ciphertext)
    print(ciphertext_b64)

    # encode and output the sound
    audio.encode_sound(ciphertext_b64)

# decode and decrypt the sound waves into message
def receive_message():
    print("Hello from listen sound!")

    # Listen and decode the sound
    ciphertext_b64 = audio.decode_sound()
    # ciphertext_b64 = "CejogwNL9MfabLgEJOtbgMa6MtDgFllC4r8BAfDlzyc="
    key = b"mysecretkey12345"

    if not ciphertext_b64:
        print("Error: Failed to decode sound into text.")
        return

    # Ensure correct Base64 decoding
    try:
        ciphertext_bytes = base64.b64decode(ciphertext_b64)  # Correct Base64 decoding
    except Exception as e:
        print(f"Base64 decoding error: {e}")
        return

    # Decrypt the message
    try:
        plaintext = aes.decrypt_data(ciphertext_bytes, key)
        print("Decrypted Message:", plaintext)
    except Exception as e:
        print(f"Decryption error: {e}")

def main():
    print("Hello from main!")

    # ask if the user want to send or listen
    choice = input("Do you want to send [S] or listen [L] message?: ")

    # call the function according to the user choice
    if choice == "S":
        send_message()
    elif choice == "L":
        receive_message()


if __name__ == "__main__":
    main()