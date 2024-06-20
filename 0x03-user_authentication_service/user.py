#!/usr/bin/env python3
"""
SQLAlchemy model definition for the 'User' corresponding to the "users" database table.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
)

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy User model representing the 'users' table.

    Attributes:
        id (int): Primary key, unique identifier
         for each user.
        email (str): The user's email address.
         This field is required.
        hashed_password (str): The user's hashed
         password. This field is required.
        session_id (str): Optional session ID
        for the user's current session.
        reset_token (str): Optional token for
         password reset functionality.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
