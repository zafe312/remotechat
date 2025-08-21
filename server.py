import os
import subprocess
from flask import Flask, request, jsonify

API_KEY = "mysecret123"  # change this

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    # Call ollama CLI
    result = subprocess.run(
        ["ollama", "run", "llama3.2:latest"],
        input=user_input.encode(),
        stdout=subprocess.PIPE,
    )

    return jsonify({"response": result.stdout.decode()})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)