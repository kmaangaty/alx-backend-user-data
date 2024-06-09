#!/usr/bin/env python3
"""Module for Index views.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_api_status() -> str:
    """GET /api/v1/status
    Returns:
        str: The status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def get_api_stats() -> str:
    """GET /api/v1/stats
    Returns:
        str: The number of each object.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized_error() -> None:
    """GET /api/v1/unauthorized
    Returns:
        None: Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden_error() -> None:
    """GET /api/v1/forbidden
    Returns:
        None: Forbidden error.
    """
    abort(403)
