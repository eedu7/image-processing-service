import time
from typing import Any, Dict, Tuple

from jose import JWTError, jwt

from app.schemas.responses.token import Token
from core.config import config
from core.exceptions import BadRequestException


class JWTTokenHandler:
    def __init__(self):
        self.SECRET_KEY = config.JWT_SECRET_KEY
        self.ALGORITHM = config.JWT_ALGORITHM
        self.EXPIRE = int(time.time()) * config.JWT_EXPIRY

    def encode_token(self, payload: Dict[str, Any]):
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

    def generate_token(self, payload: Dict[str, Any]) -> Token:
        payload["exp"] = self.EXPIRE
        access_token = self.encode_token(payload)
        payload["sub"] = "refresh_token"
        refresh_token = self.encode_token(payload)
        return Token(
            access_token=access_token, refresh_token=refresh_token, exp=payload["exp"]
        )
