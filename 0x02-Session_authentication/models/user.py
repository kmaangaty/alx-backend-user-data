#!/usr/bin/env python3
"""User module for the API.
"""
import hashlib
from models.base import Base


class User(Base):
    """User class representing users in the API.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Getter for the password attribute.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Setter for the password attribute.

        Encrypts the password using SHA256.

        Args:
            pwd (str): The password to set.

        WARNING: In real-world projects, consider using a stronger
        password hashing algorithm like argon2 or bcrypt.
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Validate a password.

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
        """Display the user's name.

        Returns:
            str: The user's name based on email/first_name/last_name.
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
