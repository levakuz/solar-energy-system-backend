from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "device" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "power_peak" VARCHAR(255),
    "orientation" VARCHAR(255),
    "count" VARCHAR(255),
    "device_type_id" INT NOT NULL REFERENCES "device_type" ("id") ON DELETE CASCADE,
    "location_id" INT NOT NULL REFERENCES "location" ("id") ON DELETE CASCADE,
    "project_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "device";"""
