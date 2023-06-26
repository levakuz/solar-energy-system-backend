from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" RENAME COLUMN "power_peak" TO "tilt";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" RENAME COLUMN "tilt" TO "power_peak";"""
