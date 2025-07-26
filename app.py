from flask import Flask, request, jsonify, render_template, redirect, session
from flask import Flask
from flask_cors import CORS
from supabase import create_client, Client
import os
import hashlib
import bo

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

#SUPABASE_URL = os.getenv("SUPABASE_URL")
#SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNicmRqam16aGpwdnN0ZW1pamxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NzA0MzgsImV4cCI6MjA2ODI0NjQzOH0.iGLLFZzrNLg6h9ribuINkocqaT6f0hwKXPCFuyXCW28"
SUPABASE_URL = "https://sbrdjjmzhjpvstemijlc.supabase.co/"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Missing email or password."

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # Debug print to see values in terminal
        print(f"[DEBUG] Login Attempt: {email} / {hashed_pw}")

        # Supabase check
        response = supabase.table('users').select('*').eq('email', email).eq('password', hashed_pw).execute()

        if response.data:
            session['user'] = email
            return redirect('/afterlogin')
        else:
            return "Login failed. Check email or password."

    # GET request — just show the form
    return render_template("logincp.html")


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        return "Missing fields."

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # Insert into Supabase
    response = supabase.table('users').insert({
        "name": name,
        "email": email,
        "password": hashed_pw
    }).execute()

    print(f"[DEBUG] Supabase register response: {response.data}")
    return redirect('/login')


@app.route('/afterlogin')
def afterlogin():
    if 'user' in session:
        return render_template("index.html", user=session['user'])
    else:
        return redirect('/login')


# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401

    data = request.get_json()
    user_input = data.get("message", "")

    # Spell correction (from bo.py)
    corrected_input = ' '.join([
        next(iter(bo.spell.candidates(word)), word)
        for word in user_input.split()
    ])

    # Get bot response
    response = bo.custom_response(corrected_input)

    # Store chat in Supabase
    supabase.table('chat_history').insert({
        "email": session['user'],
        "user_msg": user_input,
        "bot_msg": response
    }).execute()

    return jsonify({"reply": response})

@app.route("/chat/history")
def chat_history():
    if 'user' not in session:
        return redirect('/login')

    response = supabase.table('chat_history').select('*').eq('email', session['user']).order('timestamp', desc=True).execute()
    return render_template("chat_history.html", messages=response.data)


# Main entry (for local testing only — Gunicorn is used in Railway)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides PORT
    app.run(host="0.0.0.0", port=port)
