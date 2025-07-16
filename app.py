from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase import create_client, Client
import os
import hashlib
import bo

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

SUPABASE_URL = os.getenv("https://sbrdjjmzhjpvstemijlc.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNicmRqam16aGpwdnN0ZW1pamxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NzA0MzgsImV4cCI6MjA2ODI0NjQzOH0.iGLLFZzrNLg6h9ribuINkocqaT6f0hwKXPCFuyXCW28")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Serve index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Serve static files (JS, CSS, images)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        response = supabase.table('users').select('*').eq('email', email).eq('password', hashed_pw).execute()

        if response.data:
            session['user'] = email
            return redirect('/afterlogin')
        else:
            return "Login failed. Check email or password."

    return render_template('logincp.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # Save to Supabase
    supabase.table('users').insert({
        "name": name,
        "email": email,
        "password": hashed_pw
    }).execute()

    return redirect('/login')

@app.route('/afterlogin')
def afterlogin():
    if 'user' in session:
        return f"Welcome {session['user']}!"
    else:
        return redirect('/login')


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
