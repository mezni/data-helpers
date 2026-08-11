from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings


_client: AsyncMongoClient | None = None
_database: AsyncDatabase | None = None


async def connect_to_mongodb() -> None:
    global _client, _database

    if _client is not None:
        return

    _client = AsyncMongoClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=5000,
    )

    await _client.admin.command("ping")

    _database = _client[settings.mongodb_database]


async def close_mongodb_connection() -> None:
    global _client, _database

    if _client is not None:
        await _client.close()

    _client = None
    _database = None


def get_database() -> AsyncDatabase:
    if _database is None:
        raise RuntimeError(
            "MongoDB is not initialized. "
            "connect_to_mongodb() must run first."
        )

    return _database
