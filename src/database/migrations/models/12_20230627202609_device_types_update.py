from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device_type" ADD "efficiency" DOUBLE PRECISION NOT NULL;
        ALTER TABLE "device_type" ADD "photo" TEXT NOT NULL;
        ALTER TABLE "device_type" ALTER COLUMN "area" SET NOT NULL;
        ALTER TABLE "device_type" ALTER COLUMN "area" TYPE DOUBLE PRECISION USING "area"::DOUBLE PRECISION;
        ALTER TABLE "device_type" ALTER COLUMN "system_loss" TYPE DOUBLE PRECISION USING "system_loss"::DOUBLE PRECISION;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device_type" DROP COLUMN "efficiency";
        ALTER TABLE "device_type" DROP COLUMN "photo";
        ALTER TABLE "device_type" ALTER COLUMN "area" DROP NOT NULL;
        ALTER TABLE "device_type" ALTER COLUMN "area" TYPE VARCHAR(255) USING "area"::VARCHAR(255);
        ALTER TABLE "device_type" ALTER COLUMN "system_loss" TYPE VARCHAR(255) USING "system_loss"::VARCHAR(255);"""
