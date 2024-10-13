from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__: str = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"User: ID={self.id}, Name={self.name}, Email={self.email}"

    def __str__(self) -> str:
        return self.__repr__()
