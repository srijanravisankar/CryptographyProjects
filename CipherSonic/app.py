from flask import Flask, render_template, request, jsonify
import rsa  # Import rsa.py where public key handling is done

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Web UI

# Endpoint for sending/receiving the public key
@app.route("/public_key", methods=["POST"])
def public_key():
    action = request.json["action"]
    
    if action == "send":
        rsa.share_url()  # Host public key & send link via sound
        return jsonify({"status": "Public key shared!"})
    
    elif action == "receive":
        rsa.get_url()  # Receive public key via sound
        return jsonify({"status": "Public key received!"})
    
    return jsonify({"error": "Invalid action!"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
