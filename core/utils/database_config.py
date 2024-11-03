from typing import Optional

from core.config import config


def get_database_url(
    user: Optional[str] = config.MYSQL_USER,
    password: Optional[str] = config.MYSQL_PASSWORD,
    database: Optional[str] = config.MYSQL_DATABASE,
    host: str = "127.0.0.1",
    driver: str = "aiomysql",
) -> str:
    database_url: str = f"mysql+{driver}://{user}:{password}@{host}/{database}"
    return database_url
