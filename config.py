from pydantic_settings import BaseSettings


class ConfigSettings(BaseSettings):
    MYSQL_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"  # Add a default value if necessary
    JWT_EXPIRY: int = 60 * 24 * 7  # 1 week expiry by default

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


config: ConfigSettings = ConfigSettings()
