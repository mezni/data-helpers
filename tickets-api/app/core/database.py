from pymongo import AsyncMongoClient

from app.core.config import settings


class Database:
    client: AsyncMongoClient | None = None
    database = None


db = Database()


async def connect_to_mongodb() -> None:
    db.client = AsyncMongoClient(settings.mongodb_url)

    await db.client.admin.command("ping")

    db.database = db.client[settings.mongodb_database]


async def close_mongodb_connection() -> None:
    if db.client is not None:
        await db.client.close()


def get_database():
    if db.database is None:
        raise RuntimeError("MongoDB is not initialized")

    return db.database
