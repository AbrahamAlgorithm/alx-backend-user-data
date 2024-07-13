#!/usr/bin/env python3
'''
Basic Auth module
'''
from .auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    '''
     class BasicAuth that inherits from Auth
     '''

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        extracts base64 from header
        """
        if authorization_header is None or not isinstance(
                authorization_header,
                str) or not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        returns the decoded value of a Base64 string
        '''
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            bs = base64_authorization_header.encode('utf-8')
            return base64.b64decode(bs).decode('utf-8')

        except BaseException:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        return email and password
        """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str) or not (
                ":" in decoded_base64_authorization_header):
            return (None, None)
        user_details = decoded_base64_authorization_header.split(":")
        new_list = []
        username = user_details[0]
        new_list.append(username)
        user_details.pop(0)
        new_list.append(":".join(user_details))
        return tuple(new_list)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password.
        '''
        if user_email is None or not isinstance(
            user_email, str) or user_pwd is None or not isinstance(
                user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if len(users) < 1:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except BaseException:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        authorized_header = self.authorization_header(request)
        extracted = self.extract_base64_authorization_header(authorized_header)
        decoded = self.decode_base64_authorization_header(extracted)
        user_info = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(user_info[0], user_info[1])
