from app.core.config import settings


def test_settings_have_application_name() -> None:
    assert settings.app_name == "Ticket Management API"


def test_settings_have_mongodb_configuration() -> None:
    assert settings.mongodb_uri
    assert settings.mongodb_database
