#!/usr/bin/env python3
"""User module"""

import hashlib
from models.base import Base


class User(Base):
    """User class for managing user objects"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                email (str): Email address of the user.
                _password (str): Encrypted password of the user.
                first_name (str): First name of the user.
                last_name (str): Last name of the user.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Getter method for the password"""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Setter method for setting a new password

        Args:
            pwd (str): The new password to set.
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Validate a password

        Args:
            pwd (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        return hashlib.sha256(pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Display the user's name based on email, first name, and last name"""
        if not any([self.email, self.first_name, self.last_name]):
            return ""
        if not self.first_name and not self.last_name:
            return "{}".format(self.email)
        if not self.last_name:
            return "{}".format(self.first_name)
        if not self.first_name:
            return "{}".format(self.last_name)
        return "{} {}".format(self.first_name, self.last_name)
