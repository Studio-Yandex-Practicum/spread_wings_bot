from pydantic import BaseSettings


class Settings(BaseSettings):
    host = 'jetrai.online'
    user = 'root'
    password = 'YP_2023-05'
    debug: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
