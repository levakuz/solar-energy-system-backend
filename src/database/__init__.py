from tortoise import Tortoise

from src.settings import Settings


async def init_database(create_db: bool):
    await Tortoise.init(
        db_url=Settings().db_url,
        modules={'models': ['src.database.models']},
        _create_db=create_db
    )
