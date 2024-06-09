#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class.

    Attributes:
        user_id_by_session_id (dict): A dictionary mapping session IDs to user IDs.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID.
        """
        if type(user_id) == str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID.
        """
        if type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Retrieves the user associated with the request.

        Args:
            request: The request object.

        Returns:
            User: The user associated with the request.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroys an authenticated session.

        Args:
            request: The request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
