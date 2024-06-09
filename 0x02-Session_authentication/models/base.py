#!/usr/bin/env python3
"""Module for handling base objects"""

from datetime import datetime
from typing import TypeVar, List, Iterable, Dict
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    """Base class for objects"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                id (str): The ID of the object.
                created_at (str): The creation timestamp of the object.
                updated_at (str): The last update timestamp of the object.
        """
        class_name = str(self.__class__.__name__)
        if DATA.get(class_name) is None:
            DATA[class_name] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Check equality

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if objects are equal, False otherwise.
        """
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> Dict:
        """Convert the object to a JSON dictionary

        Args:
            for_serialization (bool): Whether to include all attributes or only public ones.

        Returns:
            dict: A dictionary representation of the object.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """Load all objects from file"""
        class_name = cls.__name__
        file_path = f".db_{class_name}.json"
        DATA[class_name] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[class_name][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """Save all objects to file"""
        class_name = cls.__name__
        file_path = f".db_{class_name}.json"
        objs_json = {}
        for obj_id, obj in DATA[class_name].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """Save current object"""
        class_name = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[class_name][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove object"""
        class_name = self.__class__.__name__
        if DATA[class_name].get(self.id) is not None:
            del DATA[class_name][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count all objects"""
        class_name = cls.__name__
        return len(DATA[class_name])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all objects"""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Return one object by ID"""
        class_name = cls.__name__
        return DATA[class_name].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search all objects with matching attributes"""
        class_name = cls.__name__

        def _search(obj):
            if not attributes:
                return True
            for k, v in attributes.items():
                if getattr(obj, k) != v:
                    return False
            return True

        return list(filter(_search, DATA[class_name].values()))
