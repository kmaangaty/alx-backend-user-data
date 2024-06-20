#!/usr/bin/env python3
"""
Main file for testing the Flask authentication endpoints.
"""
import requests

def register_user(email: str, password: str) -> None:
    """
    Test registration of a user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    response = requests.post('http://127.0.0.1:5000/users',
                             data={'email': email, 'password': password})
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "user created"}
    else:
        assert response.status_code == 400
        assert response.json() == {"message": "email already registered"}


def login_wrong_password(email: str, password: str) -> None:
    """
    Test login with incorrect credentials.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    response = requests.post('http://127.0.0.1:5000/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def profile_unlogged() -> None:
    """
    Test profile access without being logged in.

    Returns:
        None
    """
    response = requests.get('http://127.0.0.1:5000/profile')
    assert response.status_code == 403


def login(email: str, password: str) -> str:
    """
    Test login with correct credentials.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session_id of the user.
    """
    response = requests.post('http://127.0.0.1:5000/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    Test profile access while being logged in.

    Args:
        session_id (str): The session_id of the user.

    Returns:
        None
    """
    cookies = {'session_id': session_id}
    response = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)
    assert response.status_code == 200


def logout(session_id: str) -> None:
    """
    Test logout with the given session_id.

    Args:
        session_id (str): The session_id of the user.

    Returns:
        None
    """
    cookies = {'session_id': session_id}
    response = requests.delete('http://127.0.0.1:5000/sessions', cookies=cookies)
    if response.status_code == 302:
        assert response.url == 'http://127.0.0.1:5000/'
    else:
        assert response.status_code == 200


def get_reset_password_token(email: str) -> str:
    """
    Test getting a reset password token with the given email.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset_token of the user.
    """
    response = requests.post('http://127.0.0.1:5000/reset_password',
                             data={'email': email})
    if response.status_code == 200:
        return response.json()['reset_token']
    assert response.status_code == 401


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test updating the password with the given email, reset_token, and new_password.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset_token of the user.
        new_password (str): The new password of the user.

    Returns:
        None
    """
    data = {'email': email, 'reset_token': reset_token, 'new_password': new_password}
    response = requests.put('http://127.0.0.1:5000/reset_password', data=data)
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "Password updated"}
    else:
        assert response.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWORD = "b4l0u"
NEW_PASSWORD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWORD)
    login_wrong_password(EMAIL, NEW_PASSWORD)
    profile_unlogged()
    session_id = login(EMAIL, PASSWORD)
    profile_logged(session_id)
    logout(session_id)
    reset_token = get_reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWORD)
    login(EMAIL, NEW_PASSWORD)
