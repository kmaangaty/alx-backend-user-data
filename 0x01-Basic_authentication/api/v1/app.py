#!/usr/bin/env python3
"""API module
"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

from api.v1.views import app_views
app.register_blueprint(app_views)

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

auth = None
AUTH_TYPE = os.getenv('AUTH_TYPE')
if AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Handler for 401 errors
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Handler for 403 errors
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """ Before request handler
    """
    if auth:
        excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if not auth.require_auth(request.path, excluded_paths):
            return
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
