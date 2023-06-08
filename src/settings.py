from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    MONGO_IP: str = 'localhost'
    MONGO_USER: str = 'admin'
    MONGO_PORT: int = 27017
    MONGO_PASSWORD: str = 'admin'
    MONGO_SCHEDULE_TASKS_DB_NAME: str = 'scheduler'
    MONGO_SCHEDULE_TASKS_COLLECTION_NAME: str = 'jobs'
    MONGO_WEATHER_DATA_DB_NAME: str = 'weather_data'
    SCHEDULER_URL: str = f'mongodb://' \
                         f'{MONGO_USER}:' \
                         f'{MONGO_PASSWORD}@' \
                         f'{MONGO_IP}:' \
                         f'{MONGO_PORT}' \
                         f'/?authSource=admin&directConnection=true&ssl=false'

    BEANIE_URL: str = f'mongodb://' \
                      f'{MONGO_USER}:' \
                      f'{MONGO_PASSWORD}@' \
                      f'{MONGO_IP}:' \
                      f'{MONGO_PORT}/' \
                      f'{MONGO_WEATHER_DATA_DB_NAME}' \
                      f'?authSource=admin&directConnection=true&ssl=false'

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
                    "src.device_types.models",
                    "src.locations.models",
                    "aerich.models"
                ],
                "default_connection": "default",
            },
        }}

    MONGO_SETTINGS: MongoSettings = MongoSettings()

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
