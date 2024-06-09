#!/usr/bin/env python3
"""Session authentication with expiration
and storage support module for the API.
"""
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with expiration and storage support.

    Attributes:
        session_duration (int): The duration of the session in seconds.
    """

    def create_session(self, user_id=None) -> str:
        """Creates and stores a session ID for the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        current_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        expiration_time = sessions[0].created_at + time_span
        if expiration_time < current_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.

        Args:
            request: The request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
