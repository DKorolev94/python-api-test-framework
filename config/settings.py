import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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
    TESTIT_URL: str = "https://testit.example.com/projects/1/tests/{testit_id}"

    # Database (optional)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "testdb"
    DB_USER: str = "testuser"
    DB_PASSWORD: str = "testpassword"
    DB_SSH_HOST: str = ""
    DB_SSH_PORT: int = 22
    DB_SSH_USER: str = ""
    DB_SSH_KEY_FILE: str = "~/.ssh/id_rsa"


def get_settings() -> Settings:
    root = os.path.dirname(os.path.dirname(__file__))
    base_env = os.path.join(root, ".env")
    if os.path.exists(base_env):
        load_dotenv(base_env, override=True)
    return Settings()


settings = get_settings()
