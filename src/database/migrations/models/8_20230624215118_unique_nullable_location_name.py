from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "location" ALTER COLUMN "name" DROP NOT NULL;
        CREATE UNIQUE INDEX "uid_location_name_78638f" ON "location" ("name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_location_name_78638f";
        ALTER TABLE "location" ALTER COLUMN "name" SET NOT NULL;"""
