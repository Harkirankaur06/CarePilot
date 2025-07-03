from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
import bo
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    # Typo correction
    corrected_input = ' '.join([
        bo.spell.candidates(word).pop() if bo.spell.candidates(word) else word
        for word in user_input.split()
    ])

    response = bo.custom_response(corrected_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
