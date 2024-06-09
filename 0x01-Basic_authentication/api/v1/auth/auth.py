#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, request_path: str, excluded_paths: List[str]) -> bool:
        """
        Method to validate if the endpoint requires authentication.

        Args:
            request_path (str): The path of the request.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if request_path is None or excluded_paths is None or not excluded_paths:
            return True

        request_path_length = len(request_path)
        if request_path_length == 0:
            return True

        is_slash_terminated = request_path[-1] == '/'

        normalized_path = request_path
        if not is_slash_terminated:
            normalized_path += '/'

        for excluded_path in excluded_paths:
            excluded_path_length = len(excluded_path)
            if excluded_path_length == 0:
                continue

            if excluded_path[-1] != '*':
                if normalized_path == excluded_path:
                    return False
            else:
                if excluded_path[:-1] == request_path[:excluded_path_length - 1]:
                    return False

        return True

    def authorization_header(self, req=None) -> str:
        """
        Method that handles authorization header extraction.

        Args:
            req (flask.Request, optional): The request object. Defaults to None.

        Returns:
            str: The value of the Authorization header if present, None otherwise.
        """
        if req is None:
            return None

        return req.headers.get("Authorization", None)


    def current_user(self, req=None) -> TypeVar('User'):
        """
        Method to validate the current user.

        Args:
            req (flask.Request, optional): The request object. Defaults to None.

        Returns:
            TypeVar('User'): The user object if validation is successful, None otherwise.
        """
        return None
