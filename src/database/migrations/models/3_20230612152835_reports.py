from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "report" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_from" TIMESTAMPTZ NOT NULL,
    "date_to" TIMESTAMPTZ NOT NULL,
    "value" VARCHAR(255) NOT NULL,
    "project_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "report";"""
