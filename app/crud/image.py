from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import Image
from core.crud import BaseCRUD


class ImageCRUD(BaseCRUD[Image]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(model=Image, db_session=db_session)
