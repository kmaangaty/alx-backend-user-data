#!/usr/bin/env python3
""" Base model module
"""
import json
import os


class BaseModel:
    """ Base class for all models
    """
    def __init__(self, *args, **kwargs):
        """ Initialization of the base model """
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def to_json(self):
        """ Convert instance to JSON format """
        return json.dumps(self.__dict__)

    @classmethod
    def count(cls):
        """ Count the number of instances """
        # Mock count method; replace with actual implementation
        return 1
