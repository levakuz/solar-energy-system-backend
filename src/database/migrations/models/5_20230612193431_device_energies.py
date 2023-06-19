from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "report" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "report" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "report" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "report" ALTER COLUMN "value" TYPE DOUBLE PRECISION USING "value"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE DOUBLE PRECISION USING "power_peak"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE DOUBLE PRECISION USING "power_peak"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE DOUBLE PRECISION USING "power_peak"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE DOUBLE PRECISION USING "power_peak"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE DOUBLE PRECISION USING "orientation"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE DOUBLE PRECISION USING "orientation"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE DOUBLE PRECISION USING "orientation"::DOUBLE PRECISION;
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE DOUBLE PRECISION USING "orientation"::DOUBLE PRECISION;
        CREATE TABLE IF NOT EXISTS "device_energy" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" TIMESTAMPTZ NOT NULL,
    "value" DOUBLE PRECISION,
    "device_id" INT NOT NULL REFERENCES "device" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE VARCHAR(255) USING "power_peak"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE VARCHAR(255) USING "power_peak"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE VARCHAR(255) USING "power_peak"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "power_peak" TYPE VARCHAR(255) USING "power_peak"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE VARCHAR(255) USING "orientation"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE VARCHAR(255) USING "orientation"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE VARCHAR(255) USING "orientation"::VARCHAR(255);
        ALTER TABLE "device" ALTER COLUMN "orientation" TYPE VARCHAR(255) USING "orientation"::VARCHAR(255);
        ALTER TABLE "report" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        ALTER TABLE "report" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        ALTER TABLE "report" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        ALTER TABLE "report" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        DROP TABLE IF EXISTS "device_energy";"""
