from dotenv import find_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings app."""

    db_url: str
    telegram_token: str
    debug: bool = False

    class Config:
        """Env settings."""

        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"


settings = Settings()
