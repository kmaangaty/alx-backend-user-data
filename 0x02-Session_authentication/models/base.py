#!/usr/bin/env python3
"""Base module for the API.
"""
import json
import uuid
from os import path
from datetime import datetime
from typing import TypeVar, List, Iterable


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base():
    """Base class for API models.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance.
        """
        class_name = str(self.__class__.__name__)
        if DATA.get(class_name) is None:
            DATA[class_name] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                 TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                 TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Equality comparison for Base objects.
        """
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert the object to a JSON dictionary.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """Load all objects from file.
        """
        class_name = cls.__name__
        file_path = f".db_{class_name}.json"
        DATA[class_name] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as file:
            objs_json = json.load(file)
            for obj_id, obj_json in objs_json.items():
                DATA[class_name][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """Save all objects to file.
        """
        class_name = cls.__name__
        file_path = f".db_{class_name}.json"
        objs_json = {}
        for obj_id, obj in DATA[class_name].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(file_path, 'w') as file:
            json.dump(objs_json, file)

    def save(self):
        """Save the current object.
        """
        class_name = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[class_name][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove the object.
        """
        class_name = self.__class__.__name__
        if DATA[class_name].get(self.id) is not None:
            del DATA[class_name][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count all objects of this type.
        """
        class_name = cls.__name__
        return len(DATA[class_name].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all objects of this type.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Return one object by ID.
        """
        class_name = cls.__name__
        return DATA[class_name].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search all objects with matching attributes.
        """
        class_name = cls.__name__
        def _search(obj):
            if len(attributes) == 0:
                return True
            for key, value in attributes.items():
                if getattr(obj, key) != value:
                    return False
            return True

        return list(filter(_search, DATA[class_name].values()))
