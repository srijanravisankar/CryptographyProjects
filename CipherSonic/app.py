# from flask import Flask, render_template, request, jsonify
# import rsa  # Handles key exchange
# import main  # Contains share_key() and get_key()

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")  # Web UI

# # Public Key Exchange Endpoint
# @app.route("/public_key", methods=["POST"])
# def public_key():
#     action = request.json["action"]
#     if action == "send":
#         rsa.share_url()  # Send public key via sound
#         return jsonify({"status": "Public key shared!"})
#     elif action == "receive":
#         rsa.get_url()  # Receive public key via sound
#         return jsonify({"status": "Public key received!"})
#     return jsonify({"error": "Invalid action!"}), 400

# # AES Key Exchange Endpoint
# @app.route("/aes_key", methods=["POST"])
# def aes_key():
#     action = request.json["action"]
#     if action == "send":
#         main.share_key()  # Send AES key
#         return jsonify({"status": "AES key shared!"})
#     elif action == "receive":
#         main.get_key()  # Receive AES key
#         return jsonify({"status": "AES key received!"})
#     return jsonify({"error": "Invalid action!"}), 400

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, render_template, request, jsonify
import rsa
import main
import audio
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Web UI

# Public Key Exchange
@app.route("/public_key", methods=["POST"])
def public_key():
    action = request.json["action"]
    if action == "send":
        rsa.share_url()  # Send public key via sound
        return jsonify({"status": "Public key shared!"})
    elif action == "receive":
        rsa.get_url()  # Receive public key via sound
        return jsonify({"status": "Public key received!"})
    return jsonify({"error": "Invalid action!"}), 400

# AES Key Exchange
@app.route("/aes_key", methods=["POST"])
def aes_key():
    action = request.json["action"]
    if action == "send":
        main.share_key()  # Send AES key
        return jsonify({"status": "AES key shared!"})
    elif action == "receive":
        main.get_key()  # Receive AES key
        return jsonify({"status": "AES key received!"})
    return jsonify({"error": "Invalid action!"}), 400

# Message Sending
@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.json["message"]

    # Save message to a file
    with open("message.txt", "w") as f:
        f.write(message)

    print("🔐 Message saved as message.txt")

    # Start HTTP server to share message
    print("\nStarting HTTP server to share the message...")
    rsa.start_http_server_message(port=8003)

    return jsonify({"status": "Message link sent!"})

# Message Receiving
@app.route("/receive_message", methods=["POST"])
def receive_message():
    # Receive message URL via sound
    server_url = audio.decode_sound()

    if not server_url:
        return jsonify({"error": "Failed to receive message URL"}), 400

    print(f"🔹 Received Message URL: {server_url}")

    # Fetch the message from the server
    response = requests.get(server_url)
    if response.status_code == 200:
        message = response.text.strip()
        print(f"📩 Retrieved Message: {message}")
        return jsonify({"message": message})
    else:
        return jsonify({"error": "Failed to fetch message"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
