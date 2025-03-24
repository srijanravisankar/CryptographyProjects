# 🔐 CipherSonic: Secure Key & Message Exchange via Sound & HTTP

CipherSonic is a **secure communication system** that allows **RSA public key exchange, AES key exchange, and encrypted messaging** using **sound waves and HTTP servers**.

---

## 🚀 Features

✅ **Public Key Exchange** – Uses **RSA keys** and transmits the URL via **sound waves**.\
✅ **AES Key Exchange** – Encrypts an **AES key** using **RSA** and shares it via **HTTP & sound**.\
✅ **Encrypted Messaging** – Encrypts messages using **AES**, stores them on a **local HTTP server**, and transmits the **link via sound**.\
✅ **Web-Based Interface** – Users can send and receive messages via a **Flask web app**.

---

## 🔧 Prerequisites & Installation

### **1️⃣ Install Python (3.10 or 3.9)**

Ensure that **Python 3.9 or Python 3.10** is installed on your system.\
🔹 Check if Python is installed:

```sh
python --version
```

🔹 If not installed, download appropriate Python version from: [python.org](https://www.python.org/downloads/).

### **2️⃣ Install Required Libraries**

Run the following command to install all dependencies:

```sh
pip install flask flask-socketio eventlet requests pycryptodome pyaudio ggwave
```

### **3️⃣ Install PortAudio if needed (For Windows/Linux)**

🔹 **Windows**: Download and install PortAudio from [here](http://www.portaudio.com/download.html).\
🔹 **Linux (Debian/Ubuntu)**: Install via package manager:

```sh
sudo apt-get install portaudio19-dev
```

🔹 **Mac (Homebrew)**:

```sh
brew install portaudio
```

---

## 🎯 How to Run the Project

### **1️⃣ Start the Web App**

Run the following command in your project directory using correct python version:

```sh
py -3.10 app.py
```
Allow this app run on your computer, if any prompt appears.

📌 **This starts the Flask web app** at `http://localhost:5000`.

Now, open a **web browser** and go to:

```
http://localhost:5000
```

---

### 🔑 Key Exchange

### **2️⃣ Exchange Public Keys**

- Open **the web app (****`http://localhost:5000`****)** on both devices.
- Click **“Receive Public Key”** on one device.
  - The receiver will **listen to the sound and fetch the encrypted public key** from the server.
- Click **“Send Public Key”** on the other device.
  - The sender will **host the encrypted public key on an HTTP server** and **send the URL via sound**.

🔹 **Check if the file ****`received_public.pem`**** exists** – it stores the public key.

---

### **3️⃣ Exchange AES Key**

- Click **“Receive AES Key”** on one device.
  - The receiver will **listen for the link**, download the **encrypted AES key**, and **decrypt it using RSA private key**.
- Click **“Send AES Key”** on the other device.
  - The AES key will be **encrypted using the public key**, hosted on an **HTTP server**, and its **link sent via sound**.

🔹 **Check if the file ****`encrypted_key.pem`**** exists** – it stores the AES key.

---

## 📩 Sending & Receiving Messages

### **4️⃣ Send a Message**

- Type a message in the **text box** and click **"Send"**.
- The message is **encrypted using AES** and stored on an **HTTP server**.
- A **link to the encrypted message is transmitted via sound**.

🔹 **Check if the file ****`encrypted_message.pem`**** exists** – it stores the encrypted message.

### **5️⃣ Receive a Message**

- Before sending, click **"Receive"** to listen for the message link on the other device.
- The app **fetches the encrypted message from the server** and **decrypts it using AES**.

🔹 **The decrypted message will be displayed on the screen**.

---

## 🛠 Troubleshooting / Possible Errors

### **1️⃣ GGWave Error: Reached Maximum Instances**

**Error Message:**

```
Failed to create GGWave instance - reached maximum number of instances (4)
```

**Solution:**

1. Restart the Flask app:
   ```sh
   py -3.10 app.py
   ```
2. Ensure `ggwave.free(instance)` is called **after every sound decoding** to prevent too many instances.

---

### **2️⃣ OSError: Port Already in Use**

**Error Message:**

```
OSError: [WinError 10048] Only one usage of each socket address is normally permitted
```

**Solution:**

1. Close any previous Flask instances running on the same port.
2. Run the following command to **find and kill the process using the port** (For Windows):
   ```sh
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```
   (Replace `<PID>` with the actual process ID shown).

---

### **3️⃣ Key Exchange Fails (File Not Found Error)**

**Error Message:**

```
FileNotFoundError: No such file or directory: 'received_public.pem'
```

**Solution:**

- Ensure you **exchange public keys first** before attempting to send the AES key.
- Run **“Send Public Key”** and **“Receive Public Key”** first.

---

### **4️⃣ Message Encryption Error (****`NoneType`**** object has no attribute 'ljust')**

**Error Message:**

```
AttributeError: 'NoneType' object has no attribute 'ljust'
```

**Solution:**

- Ensure you **exchange the AES key before sending messages**.
- Run **“Send AES Key”** and **“Receive AES Key”** first.

---

```
✨ Developed by 🚀 Srijan Ravisankar
```