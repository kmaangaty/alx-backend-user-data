#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"])
def index() -> str:
    """Basic Flask route"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def register_user() -> str:
    """Register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Log in a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)

@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Log out a user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)

@app.route("/profile", methods=["GET"])
def profile() -> str:
    """Get user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
