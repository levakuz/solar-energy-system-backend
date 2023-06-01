from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Account" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone_number" VARCHAR(255)  UNIQUE,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'active',
    "password" VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "Account"."status" IS 'active: active\ninactive: inactive';
CREATE TABLE IF NOT EXISTS "CompanyAccount" (
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "account_id" INT NOT NULL  PRIMARY KEY REFERENCES "Account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "UserAccount" (
    "type" VARCHAR(9) NOT NULL  DEFAULT 'free',
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "account_id" INT NOT NULL  PRIMARY KEY REFERENCES "Account" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "UserAccount"."type" IS 'free: free\nunlimited: unlimited';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
