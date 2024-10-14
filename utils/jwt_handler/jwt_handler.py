import time
from typing import Tuple

from jose import jwt

from config import config


def encode_token(payload: dict) -> Tuple[str, int]:
    exp = int(time.time()) * config.JWT_EXPIRY
    payload["exp"] = exp
    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token, exp


def decode_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        config.JWT_SECRET_KEY,
        algorithms=[config.JWT_ALGORITHM],
    )
    return payload
