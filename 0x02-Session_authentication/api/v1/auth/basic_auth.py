#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    """

    def extract_base64_authorization_header(
            self,
            header: str) -> str:
        """Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if type(header) == str:
            pattern = r'Basic (?P<token>.+)'
            match = re.fullmatch(pattern, header.strip())
            if match is not None:
                return match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_header: str,
    ) -> str:
        """Decodes a base64-encoded authorization header.
        """
        if type(base64_header) == str:
            try:
                decoded = base64.b64decode(
                    base64_header,
                    validate=True,
                )
                return decoded.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_header: str,
    ) -> Tuple[str, str]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if type(decoded_base64_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            match = re.fullmatch(
                pattern,
                decoded_base64_header.strip(),
            )
            if match is not None:
                user = match.group('user')
                password = match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            email: str,
            password: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(email) == str and type(password) == str:
            try:
                users = User.search({'email': email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(password):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The authenticated user object, if present.
        """
        auth_header = self.authorization_header(request)
        base64_auth_token = self.extract_base64_authorization_header(auth_header)
        decoded_auth_token = self.decode_base64_authorization_header(base64_auth_token)
        user_email, user_password = self.extract_user_credentials(decoded_auth_token)
        return self.user_object_from_credentials(user_email, user_password)
