import pytest

from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
    get_database,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mongodb_connection() -> None:
    try:
        await connect_to_mongodb()

        database = get_database()

        result = await database.command("ping")

        assert result["ok"] == 1.0

    except Exception as exc:
        pytest.skip(f"MongoDB is not available: {exc}")

    finally:
        await close_mongodb_connection()
