from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = ''
    SECRET_KEY = ''
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_USER: str = 'admin'
    DB_PASSWORD: str = 'admin'
    DB_IP: str = 'localhost'
    DB_NAME: str = 'test'

    TORTOISE_ORM: dict = {
        "connections": {"default": f"asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_IP}/{DB_NAME}"},
        "apps": {
            "models": {
                "models": [
                    "src.accounts.models",
                    "aerich.models"
                ],
                "default_connection": "default",
            },
        }}

    class Config:
        fields = {
            'SECRET_KEY': {
                'env': 'SECRET_KEY'
            },
            'ALGORITHM': {
                'env': 'ALGORITHM'
            },
            'DB_PASSWORD': {
                'env': 'DB_PASSWORD'
            },
            'DB_USER': {
                'env': 'DB_USER'
            },
            'DB_IP': {
                'env': 'DB_IP'
            },
            'ACCESS_TOKEN_EXPIRE_MINUTES': {
                'env': 'ACCESS_TOKEN_EXPIRE_MINUTES'
            }
        }


settings: Settings = Settings()
TORTOISE_ORM: dict = Settings().TORTOISE_ORM
