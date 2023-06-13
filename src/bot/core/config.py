from dotenv import find_dotenv
from pydantic import AnyUrl, BaseSettings, SecretStr


class CustomDsn(AnyUrl):
    """aiomysqlDSN."""

    allowed_schemes = {"mysql+aiomysql"}


class Settings(BaseSettings):
    """Settings app."""

    db_url: CustomDsn
    telegram_token: SecretStr
    debug: bool = False
    email_host: str
    email_port: int
    email_account: str
    email_password: str
    default_email_address: str

    class Config:
        """Env settings."""

        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"


settings = Settings()
