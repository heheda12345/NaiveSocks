"""
    this module is for producing a valid password
    that for Cipher to encode and decode the data flow.
"""
import base64
import os

PASSWORD_LENGTH = 32


class InvalidPasswordError(Exception):
    """不合法的密码"""


def validatePassword(password: bytearray) -> bool:
    return len(password) == PASSWORD_LENGTH


def loadsPassword(passwordString: str) -> bytearray:
    try:
        password = base64.urlsafe_b64decode(passwordString.encode('utf8', errors='strict'))
        password = bytearray(password)
    except:
        raise InvalidPasswordError

    if not validatePassword(password):
        raise InvalidPasswordError

    return password


def loadPassword(passwordString: bytearray) -> bytearray:
    try:
        password = base64.urlsafe_b64decode(passwordString)
        password = bytearray(password)
    except:
        raise InvalidPasswordError

    if not validatePassword(password):
        raise InvalidPasswordError

    return password


def dumpsPassword(password: bytearray) -> str:
    if not validatePassword(password):
        raise InvalidPasswordError
    return base64.urlsafe_b64encode(password).decode('utf8', errors='strict')


def dumpPassword(password: bytearray) -> bytearray:
    if not validatePassword(password):
        raise InvalidPasswordError
    return base64.urlsafe_b64encode(password)


def randomPassword() -> bytearray:
    return os.urandom(PASSWORD_LENGTH)
