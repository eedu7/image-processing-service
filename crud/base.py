from typing import Any, Generic, List, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 20) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def create(self, attributes: dict[str, Any]) -> ModelType:
        if attributes is None:
            return {}

        model = self.model(**attributes)
        self.session.add(model)
        await self.session.commit()
        return model

    async def get_by(self, field: str, value: Any) -> ModelType:
        query = select(self.model).where(getattr(self.model, field) == value)
        result = await self.session.scalars(query)
        return result.first()

    async def get_by_id(self, model_id: int) -> ModelType | None:
        model = await self.get_by(field="id", value=model_id)
        if model is None:
            return None
        return model

    async def get_all_by(self, field: str, value: Any) -> List[ModelType]:
        query = select(self.model).where(getattr(self.model, field) == value)
        result = await self.session.scalars(query)
        return result.all()

    async def update(self, _id: int, attributes: dict[str, Any]) -> ModelType | None:
        model = await self.get_by(field="id", value=_id)
        if model is None:
            return None
        if attributes is None:
            return None

        for key, value in attributes.items():
            setattr(model, key, value)
        await self.session.commit()
        return model

    async def delete(self, _id: int) -> bool | None:
        model = await self.get_by(field="id", value=_id)
        if model is None:
            return None
        await self.session.delete(model)
        await self.session.commit()
        return True
