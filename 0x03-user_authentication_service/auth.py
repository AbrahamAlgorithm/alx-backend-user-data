#!/usr/bin/env python3
"""Authentication module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union

def _hash_password(Password: str) -> bytes:
    """Hash Password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

def _generate_uuid() -> str:
    '''
    generate uuid
    '''
    return str(uuid4())

class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        '''
        initialize
        '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        register user
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hass_pass = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hass_pass)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        '''
        validate user login
        '''
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        '''
        create a session for user
        Args:
            takes an email as argument
        Return:
            UUId in string format
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        uid = _generate_uuid()
        self._db.update_user(user.id, session_id=uid)
        return uid

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """
        get user from session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        '''
        destroy session
        '''
        try:
            self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        get reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            tok = _generate_uuid()
            self._db.update_user(user.id, reset_token=tok)
            return tok
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        update password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hass_p = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hass_p,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError