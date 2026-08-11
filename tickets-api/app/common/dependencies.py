from collections.abc import AsyncGenerator

from pymongo.asynchronous.database import AsyncDatabase

from app.core.database import get_database


async def get_db() -> AsyncGenerator[AsyncDatabase, None]:
    yield get_database()
