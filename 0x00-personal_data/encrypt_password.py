#!/usr/bin/env python3
"""encryption of password"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashing of Passsowrd"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''check if hashed password is the same as paaa'''
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
