import asyncio

from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
    get_database,
)


async def main() -> None:
    print("Connecting to MongoDB...")

    await connect_to_mongodb()

    database = get_database()

    result = await database.command("ping")

    print("MongoDB ping:", result)
    print("Database:", database.name)

    await close_mongodb_connection()

    print("MongoDB connection successful.")


if __name__ == "__main__":
    asyncio.run(main())
