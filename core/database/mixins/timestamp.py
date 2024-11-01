from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import MappedColumn


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamps to models."""

    @declared_attr
    def created_at(cls) -> MappedColumn:
        """Timestamp for when the record was created."""
        return MappedColumn(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls) -> MappedColumn:
        """Timestamp for when the record was last updated."""

        return MappedColumn(
            DateTime, default=func.now(), nullable=False, onupdate=func.now()
        )
