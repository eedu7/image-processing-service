from typing import AsyncIterator

from icecream import ic
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from core.utils import get_database_url
from core.utils.is_running_in_docker import is_running_in_docker

is_running_docker = is_running_in_docker()

if is_running_docker:
    DATABASE_URL: str = get_database_url(host="db")
else:
    DATABASE_URL: str = get_database_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncIterator[AsyncSession]:
    try:
        async with async_session_maker() as session:
            yield session

    except SQLAlchemyError as e:
        ic(f"Database connection error: {e}")
