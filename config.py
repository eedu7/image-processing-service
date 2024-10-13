import os
from dotenv import load_dotenv

load_dotenv()

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MYSQL_URL: str | None  = os.getenv('MYSQL_URL')
    JWT_SECRET_KEY: str | None = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM: str | None = os.getenv('JWT_ALGORITHM')


config: Config = Config()