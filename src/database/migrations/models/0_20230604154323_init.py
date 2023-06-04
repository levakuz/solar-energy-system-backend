from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "account" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone_number" VARCHAR(255)  UNIQUE,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'active',
    "password" VARCHAR(255) NOT NULL,
    "role" VARCHAR(7) NOT NULL
);
COMMENT ON COLUMN "account"."status" IS 'active: active\ninactive: inactive';
COMMENT ON COLUMN "account"."role" IS 'COMPANY: company\nUSER: user';
CREATE TABLE IF NOT EXISTS "company_account" (
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "account_id" INT NOT NULL  PRIMARY KEY REFERENCES "account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_account" (
    "type" VARCHAR(9) NOT NULL  DEFAULT 'free',
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "account_id" INT NOT NULL  PRIMARY KEY REFERENCES "account" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user_account"."type" IS 'free: free\nunlimited: unlimited';
CREATE TABLE IF NOT EXISTS "device_type" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "area" VARCHAR(255),
    "system_loss" VARCHAR(255) NOT NULL,
    "company_id" INT NOT NULL REFERENCES "company_account" ("account_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
