from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import bo

app = Flask(__name__)
CORS(app)

# Serve index.html from root
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Serve static files like JS, CSS, images
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    # Safer typo correction (avoid .pop() on empty sets)
    corrected_input = ' '.join([
        next(iter(bo.spell.candidates(word)), word)
        for word in user_input.split()
    ])

    response = bo.custom_response(corrected_input)
    return jsonify({"reply": response})

# Main entry point for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides PORT env
    app.run(host="0.0.0.0", port=port)
