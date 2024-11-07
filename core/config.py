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
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRY: int = 60 * 24
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    AWS_S3_BUCKET_NAME: str


config: Config = Config()
