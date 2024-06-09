#!/usr/bin/env python3
"""User session module for the API.
"""
from models.base import Base


class UserSession(Base):
    """User session class representing user sessions in the API.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
