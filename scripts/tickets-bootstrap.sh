#!/usr/bin/env bash

set -euo pipefail

PROJECT_NAME="${1:-ticket-management}"

echo "=========================================="
echo " Ticket Management - Project Bootstrap"
echo "=========================================="
echo
echo "Project: ${PROJECT_NAME}"
echo

# --------------------------------------------------
# Check prerequisites
# --------------------------------------------------

command -v uv >/dev/null 2>&1 || {
    echo "ERROR: uv is not installed."
    echo "Install uv: https://docs.astral.sh/uv/"
    exit 1
}

command -v docker >/dev/null 2>&1 || {
    echo "WARNING: Docker is not installed."
}

echo "uv version:"
uv --version
echo

# --------------------------------------------------
# Create project
# --------------------------------------------------

if [[ -d "${PROJECT_NAME}" ]]; then
    echo "ERROR: Directory '${PROJECT_NAME}' already exists."
    exit 1
fi

mkdir -p "${PROJECT_NAME}"
cd "${PROJECT_NAME}"

echo "Creating project..."

# --------------------------------------------------
# Initialize uv project
# --------------------------------------------------

uv init \
    --python 3.13 \
    --name "${PROJECT_NAME}"

# --------------------------------------------------
# Create directories
# --------------------------------------------------

mkdir -p \
    app/core \
    app/common \
    app/health \
    app/auth \
    app/users \
    app/tickets \
    app/comments \
    app/attachments \
    tests \
    scripts \
    docs \
    uploads

# --------------------------------------------------
# Python package files
# --------------------------------------------------

touch \
    app/__init__.py \
    app/core/__init__.py \
    app/common/__init__.py \
    app/health/__init__.py \
    app/auth/__init__.py \
    app/users/__init__.py \
    app/tickets/__init__.py \
    app/comments/__init__.py \
    app/attachments/__init__.py \
    tests/__init__.py

# --------------------------------------------------
# Install runtime dependencies
# --------------------------------------------------

echo
echo "Installing runtime dependencies..."

uv add \
    fastapi \
    "uvicorn[standard]" \
    pymongo \
    pydantic \
    pydantic-settings \
    pyjwt \
    "pwdlib[argon2]" \
    python-multipart \
    email-validator

# --------------------------------------------------
# Install development dependencies
# --------------------------------------------------

echo
echo "Installing development dependencies..."

uv add --dev \
    pytest \
    pytest-asyncio \
    httpx \
    ruff \
    mypy

# --------------------------------------------------
# Application configuration
# --------------------------------------------------

cat > app/core/config.py <<'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ticket Management API"
    app_version: str = "1.0.0"
    environment: str = "development"

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "ticket_management"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_seconds: int = 3600

    max_upload_size: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
EOF

# --------------------------------------------------
# MongoDB configuration
# --------------------------------------------------

cat > app/core/database.py <<'EOF'
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
EOF

# --------------------------------------------------
# Health router
# --------------------------------------------------

cat > app/health/router.py <<'EOF'
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    summary="Get service health",
    tags=["Health"],
)
async def health_check() -> dict:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }
EOF

# --------------------------------------------------
# Main application
# --------------------------------------------------

cat > app/main.py <<'EOF'
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
)
from app.health.router import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Ticket Management API",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

app.include_router(
    health_router,
    prefix="/api/v1",
)
EOF

# --------------------------------------------------
# Environment configuration
# --------------------------------------------------

cat > .env.example <<'EOF'
APP_NAME=Ticket Management API
APP_VERSION=1.0.0
ENVIRONMENT=development

MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=ticket_management

JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_SECONDS=3600

MAX_UPLOAD_SIZE=10485760
EOF

cp .env.example .env

# --------------------------------------------------
# Docker Compose
# --------------------------------------------------

cat > docker-compose.yml <<'EOF'
services:

  mongodb:
    image: mongo:8
    container_name: ticket-management-mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_DATABASE: ticket_management
    volumes:
      - mongodb_data:/data/db

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ticket-management-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://mongodb:27017
      MONGODB_DATABASE: ticket_management
      JWT_SECRET_KEY: change-me
      JWT_ALGORITHM: HS256
      JWT_ACCESS_TOKEN_EXPIRE_SECONDS: 3600
    depends_on:
      - mongodb

volumes:
  mongodb_data:
EOF

# --------------------------------------------------
# Dockerfile
# --------------------------------------------------

cat > Dockerfile <<'EOF'
FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# --------------------------------------------------
# Gitignore
# --------------------------------------------------

cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
.venv/

# Environment
.env
.env.*

!.env.example

# Testing
.pytest_cache/
.coverage
htmlcov/

# Type checking
.mypy_cache/

# Ruff
.ruff_cache/

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db

# Uploads
uploads/*
!uploads/.gitkeep

# Build
dist/
build/
*.egg-info/

# Logs
*.log
EOF

touch uploads/.gitkeep

# --------------------------------------------------
# Pytest configuration
# --------------------------------------------------

cat > tests/test_health.py <<'EOF'
from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/v1/")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["version"] == "1.0.0"
EOF

# --------------------------------------------------
# README
# --------------------------------------------------

cat > README.md <<EOF
# ${PROJECT_NAME}

Ticket Management API built with:

- Python 3.13+
- FastAPI
- MongoDB
- PyMongo Async
- Pydantic
- JWT
- Docker
- uv

## Development

Install dependencies:

\`\`\`bash
uv sync
\`\`\`

Start MongoDB:

\`\`\`bash
docker compose up -d mongodb
\`\`\`

Run API:

\`\`\`bash
uv run uvicorn app.main:app --reload
\`\`\`

Swagger:

http://localhost:8000/api/v1/docs

ReDoc:

http://localhost:8000/api/v1/redoc

OpenAPI:

http://localhost:8000/api/v1/openapi.json

Run tests:

\`\`\`bash
uv run pytest
\`\`\`
EOF

# --------------------------------------------------
# Ruff configuration
# --------------------------------------------------

cat >> pyproject.toml <<'EOF'

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
EOF

# --------------------------------------------------
# Format
# --------------------------------------------------

uv run ruff check . --fix
uv run ruff format .

# --------------------------------------------------
# Final output
# --------------------------------------------------

echo
echo "=========================================="
echo " Bootstrap completed successfully"
echo "=========================================="
echo
echo "Project: ${PROJECT_NAME}"
echo
echo "Next steps:"
echo
echo "  cd ${PROJECT_NAME}"
echo "  docker compose up -d mongodb"
echo "  uv run uvicorn app.main:app --reload"
echo
echo "Swagger:"
echo "  http://localhost:8000/api/v1/docs"
echo
echo "ReDoc:"
echo "  http://localhost:8000/api/v1/redoc"
echo
echo "Tests:"
echo "  uv run pytest"
echo