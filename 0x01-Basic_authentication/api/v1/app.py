#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found_error_handler(error) -> str:
    """
    Handler for 404 errors (Not Found)

    Args:
        error: The error object

    Returns:
        str: JSON response with 404 status code
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error_handler(error) -> str:
    """
    Handler for 401 errors (Unauthorized)

    Args:
        error: The error object

    Returns:
        str: JSON response with 401 status code
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error_handler(error) -> str:
    """
    Handler for 403 errors (Forbidden)

    Args:
        error: The error object

    Returns:
        str: JSON response with 403 status code
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_handler() -> str:
    """
    Before request handler for validating requests

    Returns:
        str: JSON response with the appropriate error
         status code if validation fails
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    api_host = getenv("API_HOST", "0.0.0.0")
    api_port = getenv("API_PORT", "5000")
    app.run(host=api_host, port=api_port)
