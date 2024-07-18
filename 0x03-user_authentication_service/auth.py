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