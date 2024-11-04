import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from core.database.mixins import TimestampMixin


class Image(Base, TimestampMixin):
    __tablename__ = 'image'

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[str] = mapped_column(CHAR(46), ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, User ID: {self.user_id}"

    def __str__(self):
        return self.__repr__()

