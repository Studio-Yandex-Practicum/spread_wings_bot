from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings app."""

    db_url: str = "mysql+aiomysql://root:YP_2023-05@jetrai.online/krilya_dets1"
    telegram_token: str
    debug: bool = False

    class Config:
        """Env settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
