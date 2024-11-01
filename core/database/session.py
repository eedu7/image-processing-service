from typing import AsyncIterator

from icecream import ic
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from core.config import config

DATABASE_URL: str = f"mysql+aiomysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@127.0.0.1/{config.MYSQL_DATABASE}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncIterator[AsyncSession]:
    try:
        async with async_session_maker() as session:
            yield session

    except SQLAlchemyError as e:
        ic(f"Database connection error: {e}")
