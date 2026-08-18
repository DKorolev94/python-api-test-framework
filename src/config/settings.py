from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.paths import ROOT


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из переменных окружения и файла .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    ENVIRONMENT: str
    BASE_URL: str
    GOREST_TOKEN: str
    LOG_LEVEL: str = "INFO"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "testdb"
    DB_USER: str = "testuser"
    DB_PASSWORD: str = ""
    DB_SSH_HOST: str = ""
    DB_SSH_PORT: int = 22
    DB_SSH_USER: str = ""
    DB_SSH_KEY_FILE: str = "~/.ssh/id_rsa"


def get_settings() -> Settings:
    """Загружает .env, если он есть, и создаёт экземпляр Settings."""
    base_env = ROOT / ".env"
    if base_env.exists():
        load_dotenv(base_env, override=True)
    return Settings()


settings = get_settings()
