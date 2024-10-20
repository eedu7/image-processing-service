from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MYSQL_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRY: int = 86400
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    S3_BUCKET: str
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


config: Config = Config()

