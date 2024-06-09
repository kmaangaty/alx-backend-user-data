#!/usr/bin/env python3
"""Module for user views.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """GET /api/v1/users
    Returns:
        str: JSON representation of a list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
        user_id (str): The ID of the User to retrieve.
    Returns:
        str: JSON representation of the user data.
        404 error if the User ID does not exist.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
        user_id (str): The ID of the User to delete.
    Returns:
        str: Empty JSON response if the User is successfully deleted.
        404 error if the User ID does not exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user() -> str:
    """POST /api/v1/users/
    JSON body parameters:
        - email (str): The email of the user (required).
        - password (str): The password of the user (required).
        - first_name (str): The first name of the user (optional).
        - last_name (str): The last name of the user (optional).
    Returns:
        str: JSON representation of the new user data.
        400 error if unable to create the new User.
    """
    request_json = None
    error_message = None

    try:
        request_json = request.get_json()
    except Exception:
        request_json = None

    if request_json is None:
        error_message = "Wrong format"
    if error_message is None and not request_json.get("email"):
        error_message = "email missing"
    if error_message is None and not request_json.get("password"):
        error_message = "password missing"
    if error_message is None:
        try:
            user = User()
            user.email = request_json.get("email")
            user.password = request_json.get("password")
            user.first_name = request_json.get("first_name")
            user.last_name = request_json.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_message = f"Can't create User: {e}"

    return jsonify({'error': error_message}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
        user_id (str): The ID of the User to update.
    JSON body parameters:
        - first_name (str): The first name of the user (optional).
        - last_name (str): The last name of the user (optional).
    Returns:
        str: JSON representation of the updated user data.
        404 error if the User ID does not exist.
        400 error if unable to update the User.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)

    request_json = None
    try:
        request_json = request.get_json()
    except Exception:
        request_json = None

    if request_json is None:
        return jsonify({'error': "Wrong format"}), 400

    if request_json.get('first_name') is not None:
        user.first_name = request_json.get('first_name')
    if request_json.get('last_name') is not None:
        user.last_name = request_json.get('last_name')

    user.save()
    return jsonify(user.to_json()), 200
