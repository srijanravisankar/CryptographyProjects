from flask import Flask, render_template, request, jsonify
import rsa
import main
import audio
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Public Key Exchange
@app.route("/public_key", methods=["POST"])
def public_key():
    action = request.json["action"]
    if action == "send":
        rsa.share_url()
        return jsonify({"status": "Public key shared!"})
    elif action == "receive":
        print("👂 Listening to public key ... ")
        rsa.get_url()
        return jsonify({"status": "Public key received!"})
    return jsonify({"error": "Invalid action!"}), 400

# AES Key Exchange
@app.route("/aes_key", methods=["POST"])
def aes_key():
    action = request.json["action"]
    if action == "send":
        main.share_key()
        return jsonify({"status": "AES key shared!"})
    elif action == "receive":
        print("👂 Listening to AES key ... ")
        main.get_key()
        return jsonify({"status": "AES key received!"})
    return jsonify({"error": "Invalid action!"}), 400

# Message Exchange
@app.route("/message", methods=["POST"])
def message():
    action = request.json["action"]
    if action == "send":
        message = request.json["message"]
        with open("message.txt", "w") as f:
            f.write(message)
        main.send_message(message)
        return jsonify({"status": "Message link sent!"})
    elif action == "receive":
        print("👂 Listening to messages ... ")
        message = main.receive_message()
        if not message:
            return jsonify({"error": "Failed to receive message"}), 400
        print(f"🔹 Received Message: {message}")
        return jsonify({"status": "Received: " + message})
    return jsonify({"error": "Invalid action!"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
