from app.core.database import get_database


async def check_mongodb_health() -> bool:
    database = get_database()

    await database.command("ping")

    return True
