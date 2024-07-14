#!/usr/bin/env python3
"""Aythentication method definition"""
from flask import request
from typing import TypeVar, List
from os import getenv


class Auth:
    """Authentication class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require of authentication"""
        if path is None or not path:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        path = r'{}'.format(path)
        if path[-1] == r'/':
            path = path[:-1]
        for pat in excluded_paths:
            pate = r'{}'.format(pat)
            if pate[-1] == r'/':
                pate = pate[:-1]
            if path == pate:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """The authorization header"""
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """The Crrent User"""
        return None

    def session_cookie(self, request=None):
        """Session Cookie"""
        if not request:
            return None
        value = getenv('SESSION_NAME')
        return request.cookies.get(value)
