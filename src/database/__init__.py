from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from tortoise import Tortoise

from src.settings import settings, TORTOISE_ORM


async def init_postgres_database(create_db: bool = False):
    await Tortoise.init(
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={'models': TORTOISE_ORM["apps"]["models"]["models"]},
        _create_db=create_db
    )


async def init_mongodb_database():
    client = AsyncIOMotorClient(settings.BEANIE_URL)
    await init_beanie(
        database=client.db_name,
        document_models=['src.location_weather.models.LocationWeather']
    )
