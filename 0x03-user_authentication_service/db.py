#!/usr/bin/env python3
"""
Database module for user authentication and management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class for interacting with the user database.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.

        Sets up the database engine and
         creates all tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.

        Returns:
            A SQLAlchemy Session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create and add a new User object to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by attributes.

        Args:
            **kwargs: Arbitrary keyword arguments
             representing the attributes
                      to match the user.

        Returns:
            User: The user matching the given attributes.

        Raises:
            InvalidRequestError: If any of the
            provided attributes are invalid.
            NoResultFound: If no user matches the
            given attributes.
        """
        query = self._session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid attribute: {key}")
            query = query.filter(getattr(User, key) == value)
        user = query.one_or_none()
        if user is None:
            raise NoResultFound("No user found with the given attributes")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Args:
            user_id (int): The user's ID.
            **kwargs: Arbitrary keyword arguments
             representing the attributes
                      to update and their new values.

        Returns:
            None

        Raises:
            ValueError: If the user does not exist
             or if any of the provided
                        attributes are invalid.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"No user found with ID: {user_id}")
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
