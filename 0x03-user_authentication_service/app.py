#!/usr/bin/env python3
"""
Flask app
"""
from flask import (
    Flask,
    request,
    jsonify,
    abort,
    redirect,
    url_for
)

from auth import Auth

app = Flask(__name__)
auth_service = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Return a JSON response with a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    Register a new user with the provided
    email and password.
    Returns a JSON response with the user's
     email and a success message,
    or an error message if the email is already registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth_service.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Log in a user if the provided credentials
    are correct, and create a new
    session for them. Returns a JSON response
    with the user's email and a
    success message, or an error if the credentials are invalid.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not auth_service.valid_login(email, password):
        abort(401)

    session_id = auth_service.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Log out a logged-in user and destroy their
     session. Redirects to the
    home page upon successful logout, or returns
     a 403 error if the session
    is invalid.
    """
    session_id = request.cookies.get("session_id", None)
    user = auth_service.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    auth_service.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Return a user's email based on the
     session_id in the received cookies.
    Returns a JSON response with the user's email,
     or a 403 error if the
    session is invalid.
    """
    session_id = request.cookies.get("session_id")
    user = auth_service.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generate a token for resetting a user's password.
     Returns a JSON response
    with the user's email and reset token,
    or a 403 error if the email is
    invalid.
    """
    email = request.form.get("email")
    try:
        reset_token = auth_service.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's password using the
     provided reset token and new password.
    Returns a JSON response with the user's
     email and a success message,
    or a 403 error if the reset token is invalid.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        auth_service.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
