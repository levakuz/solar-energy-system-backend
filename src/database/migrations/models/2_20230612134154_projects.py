from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "project" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'active',
    "account_id" INT NOT NULL REFERENCES "user_account" ("account_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "project"."status" IS 'active: active\ninactive: inactive';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "project";"""
