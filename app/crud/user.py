from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import BaseCRUD
from app.models import User
from core.exceptions import BadRequestException, NotFoundException
from core.utils import hash_password


class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, db_session=session)


    async def get_by_email(self, email: str) -> User | None:
        try:
            user = await super().get_by("email", email)
            return user
        except Exception as e:
            raise BadRequestException(str(e))

    async def get_by_id(self, _id: str) -> User:
        try:
            user = await super().get_by_id(_id)
            if not user:
                raise NotFoundException("User not found!")
            return user
        except Exception as e:
            raise BadRequestException(str(e))


    async def register_user(self, user_data):
        user = await self.get_by_email(user_data["email"])
        if user:
            raise BadRequestException("User already exists!")
        try:
            # Hashing password
            user_data["password"] = hash_password(user_data["password"])

            new_user = await super().create(user_data)
            if not new_user:
                raise BadRequestException("Register user failed!")
            return new_user
        except Exception as e:
            raise BadRequestException(str(e))