from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase import create_client, Client
import os
import bo

app = Flask(__name__)
CORS(app)

url = os.getenv("https://sbrdjjmzhjpvstemijlc.supabase.co")
key = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNicmRqam16aGpwdnN0ZW1pamxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NzA0MzgsImV4cCI6MjA2ODI0NjQzOH0.iGLLFZzrNLg6h9ribuINkocqaT6f0hwKXPCFuyXCW28")

supabase: Client = create_client(url, key)

# Serve index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Serve static files (JS, CSS, images)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# login page
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    result = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if result.user:
        session['user'] = result.user.id
        return redirect(url_for('dashboard'))
    else:
        return "Login failed"

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    # Safe spell correction
    corrected_input = ' '.join([
        next(iter(bo.spell.candidates(word)), word)
        for word in user_input.split()
    ])

    # Generate chatbot response
    response = bo.custom_response(corrected_input)
    return jsonify({"reply": response})

# Main entry (for local testing only — Gunicorn is used in Railway)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides PORT
    app.run(host="0.0.0.0", port=port)
