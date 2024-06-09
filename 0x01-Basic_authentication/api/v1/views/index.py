#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status() -> str:
    """
    GET /api/v1/status
    Returns the status of the API.

    Returns:
        str: JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def get_stats() -> str:
    """
    GET /api/v1/stats
    Returns the number of each object type in the system.

    Returns:
        str: JSON response with counts of various objects.
    """
    from models.user import User
    object_stats = {}
    object_stats['users'] = User.count()
    return jsonify(object_stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def trigger_unauthorized() -> None:
    """
    GET /api/v1/unauthorized
    Raises a 401 Unauthorized error.

    Returns:
        None: This function triggers a 401 error response.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def trigger_forbidden() -> None:
    """
    GET /api/v1/forbidden
    Raises a 403 Forbidden error.

    Returns:
        None: This function triggers a 403 error response.
    """
    abort(403)
