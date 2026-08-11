import pytest

from app.core import database


def test_database_is_not_initialized_by_default() -> None:
    original_database = database._database

    database._database = None

    with pytest.raises(RuntimeError):
        database.get_database()

    database._database = original_database
