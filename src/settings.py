from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings


class FastAPIMailSettings(ConnectionConfig):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_SSL_TLS: bool
    VALIDATE_CERTS: bool = False
    MAIL_STARTTLS: bool = False

    class Config:
        fields = {
            'MAIL_USERNAME': {
                'env': 'MAIL_USERNAME'
            },
            'MAIL_PASSWORD': {
                'env': 'MAIL_PASSWORD'
            },
            'MAIL_FROM': {
                'env': 'MAIL_FROM'
            },
            'MAIL_PORT': {
                'env': 'MAIL_PORT'
            },
            'MAIL_SERVER': {
                'env': 'MAIL_SERVER'
            },
            'MAIL_TLS': {
                'env': 'MAIL_TLS'
            },
            'MAIL_SSL': {
                'env': 'MAIL_SSL'
            },
        }
        env_file = '.env'
        env_file_encoding = 'utf-8'


class MongoSettings(BaseSettings):
    MONGO_IP: str = 'localhost'
    MONGO_USER: str = 'admin'
    MONGO_PORT: int = 27017
    MONGO_PASSWORD: str = 'admin'
    MONGO_SCHEDULE_TASKS_DB_NAME: str = 'scheduler'
    MONGO_SCHEDULE_TASKS_COLLECTION_NAME: str = 'jobs'
    MONGO_WEATHER_DATA_DB_NAME: str = 'weather_data'

    class Config:
        fields = {
            'MONGO_IP': {
                'env': 'MONGO_IP'
            },
            'MONGO_USER': {
                'env': 'MONGO_USER'
            },
            'MONGO_PORT': {
                'env': 'MONGO_PORT'
            },
            'MONGO_PASSWORD': {
                'env': 'MONGO_PASSWORD'
            },
            'MONGO_SCHEDULE_TASKS_DB_NAME': {
                'env': 'MONGO_SCHEDULE_TASKS_DB_NAME'
            },
            'MONGO_SCHEDULE_TASKS_COLLECTION_NAME': {
                'env': 'MONGO_SCHEDULE_TASKS_COLLECTION_NAME'
            },
            'MONGO_WEATHER_DATA_DB_NAME': {
                'env': 'MONGO_WEATHER_DATA_DB_NAME'
            },
            'MONGO_WEATHER_DATA_COLLECTION_NAME': {
                'env': 'MONGO_WEATHER_DATA_COLLECTION_NAME'
            },
        }


class Settings(BaseSettings):
    SECRET_KEY = ''
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_USER: str = 'admin'
    DB_PASSWORD: str = 'admin'
    DB_IP: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'test'
    SERVER_PORT: int = 8000

    MONGO_SETTINGS: MongoSettings = MongoSettings()
    MAIL_SETTINGS: FastAPIMailSettings = FastAPIMailSettings()
    SCHEDULER_URL: str = f'mongodb://' \
                         f'{MONGO_SETTINGS.MONGO_USER}:' \
                         f'{MONGO_SETTINGS.MONGO_PASSWORD}@' \
                         f'{MONGO_SETTINGS.MONGO_IP}:' \
                         f'{MONGO_SETTINGS.MONGO_PORT}' \
                         f'/?authSource=admin&directConnection=true&ssl=false'

    BEANIE_URL: str = f'mongodb://' \
                      f'{MONGO_SETTINGS.MONGO_USER}:' \
                      f'{MONGO_SETTINGS.MONGO_PASSWORD}@' \
                      f'{MONGO_SETTINGS.MONGO_IP}:' \
                      f'{MONGO_SETTINGS.MONGO_PORT}/' \
                      f'{MONGO_SETTINGS.MONGO_WEATHER_DATA_DB_NAME}' \
                      f'?authSource=admin&directConnection=true&ssl=false'

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
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings: Settings = Settings()
TORTOISE_ORM: dict = {
    "connections": {
        "default": f"asyncpg://"
                   f"{settings.DB_USER}"
                   f":{settings.DB_PASSWORD}"
                   f"@{settings.DB_IP}"
                   f":{settings.DB_PORT}"
                   f"/{settings.DB_NAME}"},
    "apps": {
        "models": {
            "models": [
                "src.accounts.models",
                "src.device_types.models",
                "src.locations.models",
                "src.projects.models",
                "src.reports.models",
                "src.devices.models",
                "src.device_energies.models",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    }}
