#!/usr/bin/env python3
"""
Definition of utility functions and Auth class
 for user authentication and management.
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import (
    TypeVar,
    Union
)

from db import DB
from user import User

U = TypeVar('User')


def _hash_password(password: str) -> bytes:
    """
    Hashes a password string using bcrypt and
    returns the hashed password in bytes format.

    Args:
        plain_password (str): Password in plain string format.

    Returns:
        bytes: Hashed password in bytes format.
    """
    encoded_password = password .encode('utf-8')
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns its string representation.

    Returns:
        str: A new UUID as a string.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the user authentication database.
    Provides methods for user registration, login, session management,
    password reset, and password update.
    """

    def __init__(self) -> None:
        """
        Initialize the Auth class by creating a new DB instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return the User object.

        Args:
            email (str): New user's email address.
            password (str): New user's password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user_obj = self._db.add_user(email, hashed_password)
            return user_obj
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, plain_password: str) -> bool:
        """
        Validate a user's login credentials.

        Args:
            email (str): User's email address.
            plain_password (str): User's password.

        Returns:
            bool: True if the credentials are correct, else False.
        """
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user_obj.hashed_password
        encoded_password = plain_password.encode("utf-8")
        return bcrypt.checkpw(encoded_password, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session ID for an existing user
        and update the user's session ID attribute.

        Args:
            email (str): User's email address.

        Returns:
            Union[None, str]: The created session ID,
             or None if user not found.
        """
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user_obj.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Retrieve the user corresponding to the given session ID.

        Args:
            session_id (str): Session ID.

        Returns:
            Union[None, U]: The User object if found, else None.
        """
        if session_id is None:
            return None

        try:
            user_obj = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user_obj

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user with the given
        ID by setting their session ID to None.

        Args:
            user_id (int): User's ID.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset token for the
        user identified by the given email address.

        Args:
            email (str): User's email address.

        Returns:
            str: The generated reset token.

        Raises:
            ValueError: If no user with the given email is found.
        """
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user_obj.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, plain_password: str) -> None:
        """
        Update the user's password using the
         provided reset token and new password.

        Args:
            reset_token (str): The reset token for the user.
            plain_password (str): The new password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is invalid or user not found.
        """
        try:
            user_obj = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed_password = _hash_password(plain_password)
        self._db.update_user(user_obj.id, hashed_password=hashed_password,
                             reset_token=None)
