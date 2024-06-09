#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authentication Class """

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str):
            The Authorization header value.

        Returns:
            str: The Base64 part of the Authorization header,
             None if invalid.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        encoded_part = authorization_header.split(' ', 1)[1]

        return encoded_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 encoded part of the Authorization header.

        Args:
            base64_authorization_header (str): The Base64
             encoded part of the Authorization header.

        Returns:
            str: The decoded string, None if decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            decoded_string = decoded_bytes.decode('utf-8')
        except BaseException:
            return None

        return decoded_string

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts user credentials from the Base64 decoded string.

        Args:
            decoded_base64_authorization_header (str):
             The Base64 decoded string.

        Returns:
            tuple: User email and password as a tuple,
             (None, None) if invalid.
        """

        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)

        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_password: str
    ) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_password (str): The user's password.

        Returns:
            TypeVar('User'): The User instance,
             None if authentication fails.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_password is None or not isinstance(user_password, str):
            return None

        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(user_password):
                return user

        return None

    def current_user(self, req=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves
        the User instance for a request.

        Args:
            req (flask.Request, optional):
            The request object. Defaults to None.

        Returns:
            TypeVar('User'): The User instance
             if authenticated, None otherwise.
        """
        auth_header = self.authorization_header(req)

        if not auth_header:
            return None

        encoded_part = self.extract_base64_authorization_header(auth_header)

        if not encoded_part:
            return None

        decoded_string = self.decode_base64_authorization_header(encoded_part)

        if not decoded_string:
            return None

        email, password = self.extract_user_credentials(decoded_string)

        if not email or not password:
            return None

        user = self.user_object_from_credentials(email, password)

        return user
