# app/app.py
from flask import Flask, request, render_template_string
import sqlite3
import subprocess
import os

app = Flask(__name__)
SECRET_KEY = "hardcoded-secret-123"   # 🚨 OWASP A02 — Hardcoded credential

# ── Intentional Vulnerability 1: SQL Injection (OWASP A03) ──────────────────
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # 🚨 NEVER do this — raw string interpolation = SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return {"user": result} if result else {"error": "User not found"}


# ── Intentional Vulnerability 2: Command Injection (OWASP A03) ──────────────
@app.route("/ping")
def ping_host():
    host = request.args.get("host", "localhost")
    # 🚨 NEVER do this — command injection via user input
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return {"output": result.stdout}


# ── Intentional Vulnerability 3: XSS via Template Injection (OWASP A03) ─────
@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    # 🚨 NEVER do this — XSS via unescaped user input
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)


# ── Intentional Vulnerability 4: Path Traversal (OWASP A01) ─────────────────
@app.route("/read")
def read_file():
    filename = request.args.get("file", "")
    # 🚨 NEVER do this — path traversal attack
    try:
        with open(f"./data/{filename}", "r") as f:
            return {"content": f.read()}
    except Exception as e:
        return {"error": str(e)}


# ── Intentional Vulnerability 5: Weak Cryptography (OWASP A02) ──────────────
import hashlib

@app.route("/hash")
def hash_password():
    password = request.args.get("password", "")
    # 🚨 NEVER use MD5 for passwords — it's cryptographically broken
    hashed = hashlib.md5(password.encode()).hexdigest()
    return {"hash": hashed}


if __name__ == "__main__":
    # 🚨 Debug mode in production = security risk
    app.run(debug=True, host="0.0.0.0")