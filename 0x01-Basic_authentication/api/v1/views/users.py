#!/usr/bin/env python3
""" Module for user views
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ GET /api/v1/users
    Return:
      - list of all user objects in JSON format
    """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ GET /api/v1/users/<user_id>
    Return:
      - user object in JSON format
    """
    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ POST /api/v1/users
    Return:
      - new user object in JSON format
    """
    user_data = request.get_json()
    user = User(**user_data)
    user.save()
    return jsonify(user.to_json()), 201
