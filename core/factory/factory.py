from fastapi import Depends

from app.crud.image import ImageCRUD
from app.crud.user import UserCRUD
from core.database import get_async_session


class Factory:
    """
    This is the factory container that will instantiate all the crud which can be accessed by the rest of the application.
    """

    @staticmethod
    def get_user_crud(db_session=Depends(get_async_session)):
        return UserCRUD(db_session)

    @staticmethod
    def get_image_crud(db_session=Depends(get_async_session)):
        return ImageCRUD(db_session)
