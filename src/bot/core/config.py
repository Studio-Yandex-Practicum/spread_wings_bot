from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings."""

    db_url: str = "mysql+aiomysql://root:YP_2023-05@jetrai.online/krilya_dets1"
    debug: bool = False

    class Config:
        """env settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
