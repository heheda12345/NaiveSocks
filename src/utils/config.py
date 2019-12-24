import json
import typing
from collections import namedtuple
from urllib.parse import urlparse

from core.password import (InvalidPasswordError, dumpsPassword, loadsPassword)

Config = namedtuple('Config', 'serverAddr serverPort localAddr localPort password key')


class InvalidURLError(Exception):
    """无效的config URL"""


class InvalidFileError(Exception):
    """无效的配置文件"""


def dumps(config: Config) -> str:
    return json.dumps(config._asdict(), indent=2)


def loads(string: str) -> Config:
    try:
        data = json.loads(string)
        config = Config(**data)

    except Exception:
        raise InvalidFileError

    return config


def dump(f: typing.TextIO, config: Config) -> None:
    json.dump(config._asdict(), f, indent=2)


def load(f: typing.TextIO) -> Config:
    try:
        data = json.load(f)
        config = Config(**data)

    except Exception:
        raise InvalidFileError

    return config
