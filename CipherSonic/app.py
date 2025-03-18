from flask import Flask, render_template, request, jsonify
import rsa  # Handles key exchange
import main  # Contains share_key() and get_key()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Web UI

# Public Key Exchange Endpoint
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

# AES Key Exchange Endpoint
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
