from tortoise import Tortoise

from src.settings import Settings, TORTOISE_ORM


async def init_database(create_db: bool=False):
    print(Settings().db_url)
    await Tortoise.init(
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={'models': TORTOISE_ORM["apps"]["models"]["models"]},
        _create_db=create_db
    )
