import bcrypt

def _hash_password(Password: str) -> bytes:
    """Hash Password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash