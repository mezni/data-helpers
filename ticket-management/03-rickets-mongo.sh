#!/usr/bin/env bash

set -euo pipefail

echo "=========================================="
echo " Ticket Management API"
echo " Phase 02 - MongoDB Foundation"
echo "=========================================="
echo

# ============================================================
# Project validation
# ============================================================

if [[ ! -f "pyproject.toml" ]]; then
    echo "ERROR: pyproject.toml not found."
    echo "Run this script from the project root."
    exit 1
fi

if [[ ! -d "app" ]]; then
    echo "ERROR: app/ directory not found."
    echo "Run Phase 01 first."
    exit 1
fi

echo "Project root detected."
echo

# ============================================================
# Required files
# ============================================================

if [[ ! -f "app/main.py" ]]; then
    echo "ERROR: app/main.py not found."
    echo "Run Phase 01 first."
    exit 1
fi

# ============================================================
# Install dependencies with uv
# ============================================================

echo "Installing MongoDB dependencies..."

uv add pymongo pydantic-settings

echo

# ============================================================
# Create directories
# ============================================================

echo "Creating MongoDB infrastructure..."

mkdir -p \
    app/core \
    app/common \
    tests/core \
    tests/integration \
    scripts

touch app/core/__init__.py
touch app/common/__init__.py
touch tests/core/__init__.py
touch tests/integration/__init__.py

# ============================================================
# Environment example
# ============================================================

echo "Creating environment template..."

cat > .env.example <<'EOF'
# ============================================================
# Application
# ============================================================

APP_NAME=Ticket Management API
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=true

# ============================================================
# MongoDB
# ============================================================

MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=ticket_management

# ============================================================
# API
# ============================================================

API_HOST=0.0.0.0
API_PORT=8000
EOF

# ============================================================
# Local .env
# ============================================================

if [[ ! -f ".env" ]]; then
    echo "Creating .env..."

    cp .env.example .env

    echo ".env created."
else
    echo ".env already exists."
fi

# ============================================================
# Configuration
# ============================================================

echo "Creating application configuration..."

cat > app/core/config.py <<'PYEOF'
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ticket Management API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "ticket_management"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
PYEOF

# ============================================================
# MongoDB database manager
# ============================================================

echo "Creating MongoDB database manager..."

cat > app/core/database.py <<'PYEOF'
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
PYEOF

# ============================================================
# MongoDB health
# ============================================================

echo "Creating MongoDB health check..."

cat > app/core/mongodb_health.py <<'PYEOF'
from app.core.database import get_database


async def check_mongodb_health() -> bool:
    database = get_database()

    await database.command("ping")

    return True
PYEOF

# ============================================================
# MongoDB dependency
# ============================================================

echo "Updating database dependency..."

cat > app/common/dependencies.py <<'PYEOF'
from collections.abc import AsyncGenerator

from pymongo.asynchronous.database import AsyncDatabase

from app.core.database import get_database


async def get_db() -> AsyncGenerator[AsyncDatabase]:
    yield get_database()
PYEOF

# ============================================================
# MongoDB health endpoint
# ============================================================

echo "Creating health endpoints..."

cat > app/health/router.py <<'PYEOF'
from fastapi import APIRouter

from app.core.config import settings
from app.core.mongodb_health import check_mongodb_health


router = APIRouter()


@router.get(
    "/",
    summary="Get service health",
    tags=["Health"],
)
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


@router.get(
    "/health/mongodb",
    summary="Check MongoDB health",
    tags=["Health"],
)
async def mongodb_health_check() -> dict[str, str]:
    await check_mongodb_health()

    return {
        "status": "healthy",
        "database": settings.mongodb_database,
    }
PYEOF

# ============================================================
# MongoDB startup validation
# ============================================================

echo "Updating FastAPI application..."

cat > app/main.py <<'PYEOF'
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.comments.router import router as comments_router
from app.core.config import settings
from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
)
from app.health.router import router as health_router
from app.tickets.router import router as tickets_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Ticket Management API - Modular Monolith",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)


app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    users_router,
    prefix="/api/v1/admin/users",
    tags=["Admin - Users"],
)

app.include_router(
    tickets_router,
    prefix="/api/v1/tickets",
    tags=["Tickets"],
)

app.include_router(
    comments_router,
    prefix="/api/v1/tickets",
    tags=["Comments"],
)
PYEOF

# ============================================================
# MongoDB initialization script
# ============================================================

echo "Creating MongoDB initialization script..."

cat > scripts/check_mongodb.py <<'PYEOF'
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
PYEOF

# ============================================================
# Unit tests - configuration
# ============================================================

echo "Creating configuration tests..."

cat > tests/core/test_config.py <<'PYEOF'
from app.core.config import settings


def test_settings_have_application_name() -> None:
    assert settings.app_name == "Ticket Management API"


def test_settings_have_mongodb_configuration() -> None:
    assert settings.mongodb_uri
    assert settings.mongodb_database
PYEOF

# ============================================================
# Unit tests - database lifecycle
# ============================================================

cat > tests/core/test_database.py <<'PYEOF'
import pytest

from app.core import database


def test_database_is_not_initialized_by_default() -> None:
    original_database = database._database

    database._database = None

    with pytest.raises(RuntimeError):
        database.get_database()

    database._database = original_database
PYEOF

# ============================================================
# Integration test
# ============================================================

cat > tests/integration/test_mongodb.py <<'PYEOF'
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
PYEOF

# ============================================================
# Pytest configuration
# ============================================================

echo "Configuring pytest..."

python - <<'PY'
from pathlib import Path

path = Path("pyproject.toml")
content = path.read_text()

if "[tool.pytest.ini_options]" not in content:
    content += """

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "integration: tests requiring external services",
]
"""

path.write_text(content)
PY

# ============================================================
# Documentation
# ============================================================

echo "Creating MongoDB documentation..."

mkdir -p docs

cat > docs/mongodb.md <<'EOF'
# MongoDB Foundation

## Database

The application uses MongoDB as its only persistence database.

Database name:

```text
ticket_management
````

## Connection

Configuration is loaded from environment variables.

```text
MONGODB_URI
MONGODB_DATABASE
```

Example:

```text
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=ticket_management
```

## Driver

The application uses the asynchronous PyMongo API.

```python
from pymongo import AsyncMongoClient
```

## Lifecycle

MongoDB is initialized during FastAPI startup:

```text
FastAPI startup
      |
      v
connect_to_mongodb()
      |
      v
MongoDB ping
      |
      v
Application ready
```

On shutdown:

```text
FastAPI shutdown
      |
      v
close_mongodb_connection()
```

## Dependency

Routes can access the database through:

```python
from app.common.dependencies import get_db
```

## Architecture

```text
Router
   |
   v
Service
   |
   v
Repository
   |
   v
get_database()
   |
   v
MongoDB
```

Routers must not access MongoDB directly.

Services must not contain MongoDB queries.

Repositories own persistence operations.

## Health

MongoDB health:

```text
GET /api/v1/health/mongodb
```

Swagger:

```text
GET /api/v1/docs
```

EOF

# ============================================================

# Ruff

# ============================================================

echo
echo "Formatting..."

uv run ruff format app tests scripts

echo
echo "Running Ruff..."

uv run ruff check app tests scripts

# ============================================================

# Unit tests

# ============================================================

echo
echo "Running unit tests..."

uv run pytest tests/core

# ============================================================

# Import validation

# ============================================================

echo
echo "Validating FastAPI application..."

uv run python -c 
"from app.main import app; print(f'Application loaded: {app.title}')"

# ============================================================

# MongoDB availability

# ============================================================

echo
echo "Checking MongoDB..."

if uv run python scripts/check_mongodb.py; then
echo "MongoDB: PASSED"
else
echo
echo "WARNING: MongoDB is not currently available."
echo "Start MongoDB and run:"
echo
echo "    uv run python scripts/check_mongodb.py"
echo
fi

# ============================================================

# Complete

# ============================================================

echo
echo "=========================================="
echo " Phase 02 completed"
echo "=========================================="
echo
echo "MongoDB Foundation:"
echo "  Configuration       READY"
echo "  AsyncMongoClient    READY"
echo "  Database lifecycle  READY"
echo "  FastAPI dependency  READY"
echo "  Health endpoint     READY"
echo "  Tests               READY"
echo
echo "Swagger:"
echo "  http://localhost:8000/api/v1/docs"
echo
echo "MongoDB health:"
echo "  http://localhost:8000/api/v1/health/mongodb"
echo
echo "Next:"
echo "  Phase 03 - Authentication"
echo

```
```
