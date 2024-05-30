#!/usr/bin/env python3
"""
This script defines functions to hash passwords and validate them.
"""

import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    password_bytes = password.encode()
    hashed_password = hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

