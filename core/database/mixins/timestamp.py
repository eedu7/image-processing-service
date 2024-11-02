from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps to models."""

    @declared_attr
    def created_at(cls) -> Mapped[Optional[DateTime]]:
        """Timestamp for when the record was created."""
        return mapped_column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls) -> Mapped[Optional[DateTime]]:
        """Timestamp for when the record was last updated."""

        return mapped_column(
            DateTime, default=func.now(), nullable=False, onupdate=func.now()
        )
