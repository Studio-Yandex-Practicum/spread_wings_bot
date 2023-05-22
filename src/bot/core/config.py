from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str = 'TOKEN_BOT'

    class Config:
        env_file = '.env'


settings = Settings()