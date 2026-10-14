"""Core configuration and settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "User Service"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    DATABASE_URL: str = "mysql+pymysql://user_admin:user_password@localhost:3307/user_db"
    POLL_SERVICE_URL: str = "http://localhost:8002/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
