from typing import Any, Dict, Generic, List, Sequence, Type, TypeVar

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(Generic[ModelType]):
    """
    Generic CRUD (Create, Read, Update, Delete) class for managing database operations
    on SQLAlchemy models asynchronously.

    This class provides common CRUD operations that can be inherited or instantiated
    for any SQLAlchemy model. All database operations are performed using an async
    session for asynchronous access.
    """

    def __init__(self, model: Type[ModelType], db_session: AsyncSession) -> None:
        """
        Initialize the BaseCRUD instance.

        Args:
            model (Type[ModelType]): The SQLAlchemy model class to operate on.
            db_session (AsyncSession): An async database session.
        """
        self.session = db_session
        self.model: Type[ModelType] = model

    async def get_all(self, skip: int = 0, limit: int = 20) -> Sequence[ModelType]:
        """
        Retrieve a list of all records, with optional pagination.

        Args:
            skip (int): Number of records to skip for pagination.
            limit (int): Maximum number of records to retrieve.

        Returns:
            List[ModelType]: A list of model instances.
        """
        query = select(self.model).offset(skip).limit(limit)
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, attributes: Dict[str, Any]) -> ModelType | None:
        """
        Create a new record in the database.

        Args:
            attributes (Dict[str, Any]): A dictionary of attributes to assign to the model.

        Returns:
            ModelType | None: The created model instance, or None if attributes are None.
        """
        if attributes is None:
            return None

        model = self.model(**attributes)
        self.session.add(model)
        await self.session.commit()
        return model

    async def get_by(self, field: str, value: Any) -> ModelType:
        """
        Retrieve a single record by a specified field and value.

        Args:
            field (str): The field name to filter by.
            value (Any): The value to filter the field with.

        Returns:
            ModelType: The first model instance matching the criteria.
        """
        query = select(self.model).where(
            getattr(self.model, field) == value
        )  # TODO: Adjust the types annotation
        result = await self.session.execute(query)
        return result.scalars().first()  # TODO: Adjust the types annotation

    async def get_by_id(self, _id: str) -> ModelType:
        """
        Retrieve a single record by its unique ID.

        Args:
            _id (str): The unique identifier of the record.

        Returns:
            ModelType: The model instance with the specified ID.
        """
        _model = await self.get_by(field="id", value=_id)
        return _model

    async def get_all_by(
        self, field: str, value: Any, skip: int = 0, limit: int = 20
    ) -> List[ModelType]:
        """
        Retrieve all records that match a specific field and value.

        Args:
            field (str): The field name to filter by.
            value (Any): The value to filter the field with.
            skip (int): Number of records to skip for pagination.
            limit (int): Maximum number of records to retrieve.

        Returns:
            List[ModelType]: A list of model instances matching the criteria.
        """
        query = (
            select(self.model)
            .where(getattr(self.model, field) == value)
            .offset(skip)
            .limit(limit)
        )  # TODO: Adjust the types annotation
        result = await self.session.scalars(query)
        return result.all()  # TODO: Adjust the types annotation

    async def update(self, _id: str, attributes: dict[str, Any]) -> ModelType | None:
        """
        Update an existing record by ID with specified attributes.

        Args:
            _id (str): The unique identifier of the record to update.
            attributes (dict[str, Any]): A dictionary of attributes to update on the model.

        Returns:
            ModelType | None: The updated model instance, or None if not found or attributes are None.
        """
        model = await self.get_by(field="id", value=_id)
        if model is None or attributes is None:
            return None

        for key, value in attributes.items():
            setattr(model, key, value)
        await self.session.commit()
        return model

    async def delete(self, _id: str) -> bool | None:
        """
        Delete a record by its unique ID.

        Args:
            _id (str): The unique identifier of the record to delete.

        Returns:
            bool | None: True if deletion was successful, None if the record was not found.
        """
        model = await self.get_by(field="id", value=_id)
        if model is None:
            return None
        await self.session.delete(model)
        await self.session.commit()
        return True
