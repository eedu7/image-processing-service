from sqlalchemy.ext.asyncio import AsyncSession

from crud import BaseCrud
from models import Image


class ImageCrud(BaseCrud[Image]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Image, session)

