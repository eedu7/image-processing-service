from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, MappedColumn

from db import Base


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = MappedColumn(String(255), nullable=False)

    def __str__(self) -> str:
        return f"Image: {self.id}: {self.name}"

    def __repr__(self) -> str:
        return self.__str__()
