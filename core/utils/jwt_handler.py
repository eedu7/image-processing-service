import time
from typing import Tuple, Dict, Any
from jose import jwt, JWTError

from core.config import config
from core.exceptions import BadRequestException


class JWTTokenHandler:
    def __init__(self):
        self.SECRET_KEY = config.JWT_SECRET_KEY
        self.ALGORITHM = config.JWT_ALGORITHM
        self.EXPIRE = config.JWT_EXPIRY

    def encode_token(self, payload: Dict[str, Any]):
        expiration: int = int(time.time()) + self.EXPIRE
        payload['exp'] = expiration
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload
        except JWTError as e:
            if "expired" in str(e):
                raise BadRequestException("Token has expired")
            raise BadRequestException("Invalid token")