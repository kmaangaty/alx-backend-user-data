#!/usr/bin/env python3
"""
Flask application for user authentication and management.
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
    Endpoint to check if the application is running.

    Returns:
        JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    Register a new user with the provided email and password.

    Returns:
        JSON response containing the user's email and a success message.
        If the email is already registered, returns an error message with a 400 status code.
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
    Log in a user with the provided email and password.

    Returns:
        JSON response containing the user's email and a success message.
        Sets a session cookie if login is successful.
        If the credentials are invalid, returns a 401 error.
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
    Log out a user and destroy their session.

    Returns:
        Redirects to the home page if the session is successfully destroyed.
        If the session is invalid, returns a 403 error.
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
    Retrieve the user's email based on the session_id in the cookies.

    Returns:
        JSON response containing the user's email.
        If the session is invalid, returns a 403 error.
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

    Returns:
        JSON response containing the user's email and the reset token.
        If the email is invalid, returns a 403 error.
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
    Update a user's password using the provided reset token and new password.

    Returns:
        JSON response containing the user's email and a success message.
        If the reset token is invalid, returns a 403 error.
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
