from pathlib import Path

from pydantic_settings import BaseSettings


class ConfigSettings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = Path(__file__).parent / "../.env"
        env_file_encoding = "utf-8"


class Config(ConfigSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str


config: Config = Config()
