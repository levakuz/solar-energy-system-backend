from tortoise import Tortoise

from src.settings import settings


async def init_database(create_db: bool=False):
    await Tortoise.init(
        db_url=settings.TORTOISE_ORM["connections"]["default"],
        modules={'models': settings.TORTOISE_ORM["apps"]["models"]["models"]},
        _create_db=create_db
    )
