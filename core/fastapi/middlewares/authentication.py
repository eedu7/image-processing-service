from typing import Optional, Tuple

from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import \
    AuthenticationMiddleware as BaseAuthenticationMiddleware
from starlette.requests import HTTPConnection

from app.schemas.extras import CurrentUser
from core.utils import JWTTokenHandler

class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = JWTTokenHandler().decode_token(token)
            user_id = payload.get("user_id")
        except Exception:
            return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddlewares(BaseAuthenticationMiddleware):
    pass