cat > tickets-archi.sh << 'SCRIPT_EOF'
#!/usr/bin/env bash

set -euo pipefail

echo "=========================================="
echo " Ticket Management API"
echo " Phase 01 - Application Architecture"
echo "=========================================="
echo

# --------------------------------------------------
# Verify project root
# --------------------------------------------------

if [[ ! -f "pyproject.toml" ]]; then
    echo "ERROR: pyproject.toml not found."
    echo "Run this script from the project root."
    exit 1
fi

if [[ ! -d "app" ]]; then
    echo "ERROR: app/ directory not found."
    echo "Run Phase 00 bootstrap first."
    exit 1
fi

echo "Project root detected."
echo

# --------------------------------------------------
# Create module directories
# --------------------------------------------------

echo "Creating application modules..."

mkdir -p \
    app/core \
    app/common \
    app/health \
    app/auth \
    app/users \
    app/tickets \
    app/comments \
    app/attachments \
    tests/core \
    tests/common \
    tests/health \
    tests/auth \
    tests/users \
    tests/tickets \
    tests/comments \
    tests/attachments \
    docs

# --------------------------------------------------
# Create Python package files
# --------------------------------------------------

echo "Creating Python packages..."

packages=(
    app
    app/core
    app/common
    app/health
    app/auth
    app/users
    app/tickets
    app/comments
    app/attachments
    tests
    tests/core
    tests/common
    tests/health
    tests/auth
    tests/users
    tests/tickets
    tests/comments
    tests/attachments
)

for package in "${packages[@]}"; do
    touch "${package}/__init__.py"
done

# --------------------------------------------------
# Common response models
# --------------------------------------------------

cat > app/common/responses.py <<'EOF'
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str


class ApiResponse(BaseModel, Generic[T]):
    data: T | None = None
    error: ErrorDetail | None = None
EOF

# --------------------------------------------------
# Pagination
# --------------------------------------------------

cat > app/common/pagination.py <<'EOF'
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    size: int
EOF

# --------------------------------------------------
# Common dependencies
# --------------------------------------------------

cat > app/common/dependencies.py <<'EOF'
from collections.abc import AsyncGenerator

from pymongo.asynchronous.database import AsyncDatabase

from app.core.database import get_database


async def get_db() -> AsyncGenerator[AsyncDatabase, None]:
    yield get_database()
EOF

# --------------------------------------------------
# Application exceptions
# --------------------------------------------------

cat > app/core/exceptions.py <<'EOF'
class ApplicationError(Exception):
    """Base application exception."""

    def __init__(
        self,
        code: str,
        message: str,
    ) -> None:
        self.code = code
        self.message = message

        super().__init__(message)


class NotFoundError(ApplicationError):
    """Raised when a resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
    ) -> None:
        super().__init__(code, message)


class ConflictError(ApplicationError):
    """Raised when a resource conflicts with existing state."""

    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
    ) -> None:
        super().__init__(code, message)


class ForbiddenError(ApplicationError):
    """Raised when access is not allowed."""

    def __init__(
        self,
        message: str = "Forbidden",
        code: str = "FORBIDDEN",
    ) -> None:
        super().__init__(code, message)
EOF

# --------------------------------------------------
# Exception handlers
# --------------------------------------------------

cat > app/core/exception_handlers.py <<'EOF'
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError


async def application_exception_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "data": None,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
        },
    )
EOF

# --------------------------------------------------
# Module factory helper
# --------------------------------------------------

create_module() {
    local module="$1"

    echo "Creating module: ${module}"

    touch \
        "app/${module}/router.py" \
        "app/${module}/schemas.py" \
        "app/${module}/service.py" \
        "app/${module}/repository.py"
}

# --------------------------------------------------
# Create business modules
# --------------------------------------------------

create_module "auth"
create_module "users"
create_module "tickets"
create_module "comments"
create_module "attachments"

# --------------------------------------------------
# Module documentation
# --------------------------------------------------

cat > app/auth/__init__.py <<'EOF'
"""Authentication module.

Responsible for:
- User authentication
- JWT token generation
- JWT token validation
- Current-user authentication dependencies
"""
EOF

cat > app/users/__init__.py <<'EOF'
"""User management module.

Responsible for:
- User persistence
- User administration
- User roles
"""
EOF

cat > app/tickets/__init__.py <<'EOF'
"""Ticket management module.

Responsible for:
- Ticket lifecycle
- Ticket business rules
- Ticket persistence
- Ticket authorization
"""
EOF

cat > app/comments/__init__.py <<'EOF'
"""Ticket comments module.

Responsible for:
- Creating comments
- Listing comments
- Comment persistence
"""
EOF

cat > app/attachments/__init__.py <<'EOF'
"""Ticket attachment module.

Responsible for:
- Attachment metadata
- File validation
- File storage abstraction
"""
EOF

# --------------------------------------------------
# Repository contracts
# --------------------------------------------------

cat > app/auth/repository.py <<'EOF'
"""Authentication persistence operations.

Database implementation will be added in a later phase.
"""
EOF

cat > app/users/repository.py <<'EOF'
"""User persistence operations.

Database implementation will be added in a later phase.
"""
EOF

cat > app/tickets/repository.py <<'EOF'
"""Ticket persistence operations.

Database implementation will be added in a later phase.
"""
EOF

cat > app/comments/repository.py <<'EOF'
"""Comment persistence operations.

Database implementation will be added in a later phase.
"""
EOF

cat > app/attachments/repository.py <<'EOF'
"""Attachment persistence operations.

Database implementation will be added in a later phase.
"""
EOF

# --------------------------------------------------
# Service boundaries
# --------------------------------------------------

cat > app/auth/service.py <<'EOF'
"""Authentication business logic.

HTTP concerns MUST remain in router.py.
MongoDB concerns MUST remain in repository.py.
"""
EOF

cat > app/users/service.py <<'EOF'
"""User business logic.

HTTP concerns MUST remain in router.py.
MongoDB concerns MUST remain in repository.py.
"""
EOF

cat > app/tickets/service.py <<'EOF'
"""Ticket business logic.

HTTP concerns MUST remain in router.py.
MongoDB concerns MUST remain in repository.py.
"""
EOF

cat > app/comments/service.py <<'EOF'
"""Comment business logic.

HTTP concerns MUST remain in router.py.
MongoDB concerns MUST remain in repository.py.
"""
EOF

cat > app/attachments/service.py <<'EOF'
"""Attachment business logic.

HTTP concerns MUST remain in router.py.
Storage concerns MUST remain behind a storage abstraction.
"""
EOF

# --------------------------------------------------
# Schemas
# --------------------------------------------------

cat > app/auth/schemas.py <<'EOF'
"""Authentication API schemas."""
EOF

cat > app/users/schemas.py <<'EOF'
"""User API schemas."""
EOF

cat > app/tickets/schemas.py <<'EOF'
"""Ticket API schemas."""
EOF

cat > app/comments/schemas.py <<'EOF'
"""Comment API schemas."""
EOF

cat > app/attachments/schemas.py <<'EOF'
"""Attachment API schemas."""
EOF

# --------------------------------------------------
# Routers
# --------------------------------------------------

cat > app/auth/router.py <<'EOF'
from fastapi import APIRouter


router = APIRouter()


# Authentication endpoints will be implemented in Phase 03.
EOF

cat > app/users/router.py <<'EOF'
from fastapi import APIRouter


router = APIRouter()


# User administration endpoints will be implemented in Phase 05.
EOF

cat > app/tickets/router.py <<'EOF'
from fastapi import APIRouter


router = APIRouter()


# Ticket endpoints will be implemented in Phase 06.
EOF

cat > app/comments/router.py <<'EOF'
from fastapi import APIRouter


router = APIRouter()


# Comment endpoints will be implemented in Phase 10.
EOF

cat > app/attachments/router.py <<'EOF'
from fastapi import APIRouter


router = APIRouter()


# Attachment endpoints will be implemented in Phase 11.
EOF

# --------------------------------------------------
# Health router normalization
# --------------------------------------------------

cat > app/health/router.py <<'EOF'
from fastapi import APIRouter

from app.core.config import settings


router = APIRouter()


@router.get(
    "/",
    summary="Get service health",
    description="Returns the current API service status.",
    tags=["Health"],
)
async def health_check() -> dict[str, str]:
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

# --------------------------------------------------
# Health
# --------------------------------------------------

app.include_router(
    health_router,
    prefix="/api/v1",
)

# --------------------------------------------------
# Authentication
# --------------------------------------------------

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

# --------------------------------------------------
# Users
# --------------------------------------------------

app.include_router(
    users_router,
    prefix="/api/v1/admin/users",
    tags=["Admin - Users"],
)

# --------------------------------------------------
# Tickets
# --------------------------------------------------

app.include_router(
    tickets_router,
    prefix="/api/v1/tickets",
    tags=["Tickets"],
)

# --------------------------------------------------
# Comments
# --------------------------------------------------

app.include_router(
    comments_router,
    prefix="/api/v1/tickets",
    tags=["Comments"],
)
EOF

# --------------------------------------------------
# Architecture documentation
# --------------------------------------------------

cat > docs/architecture.md <<'EOF'
# Application Architecture

## Architecture Style

The Ticket Management API is a modular monolith.

There is:

- One FastAPI application
- One deployment
- One MongoDB database

The application is internally divided into business modules.

## Modules

```text
app/
├── core/
├── common/
├── health/
├── auth/
├── users/
├── tickets/
├── comments/
└── attachments/
````

## Layering

Each business module follows:

```text
HTTP
 │
 ▼
Router
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
MongoDB
```

## Router

Responsible for:

* HTTP routes
* Request parsing
* Response serialization
* FastAPI dependencies
* HTTP status codes

Router MUST NOT:

* Query MongoDB
* Implement business rules
* Implement complex authorization logic

## Service

Responsible for:

* Business rules
* Domain behavior
* Workflow validation
* Authorization decisions
* Coordination between repositories

Service MUST NOT depend on FastAPI Request objects.

## Repository

Responsible for:

* MongoDB queries
* MongoDB writes
* MongoDB-specific persistence logic
* Database indexes

Repository MUST NOT contain HTTP logic.

## Schemas

Pydantic schemas define:

* Request models
* Response models
* Validation rules

## Core

Contains cross-cutting infrastructure:

* Configuration
* Database lifecycle
* Security
* Exceptions
* Logging

## Common

Contains reusable application infrastructure:

* Pagination
* Response models
* Shared dependencies

## Dependency Direction

Preferred dependency direction:

```text
router
  ↓
service
  ↓
repository
  ↓
database
```

Infrastructure:

```text
core
 ↑
common
 ↑
modules
```

Business modules should not depend on other modules' internal repositories.

Cross-module communication should happen through service interfaces or explicit application-level contracts.

## Business Logic Rule

Business logic belongs in services.

Example:

```text
Bad:

router
 ├── query MongoDB
 ├── check permissions
 ├── validate status
 └── update ticket

Good:

router
 └── ticket_service
       ├── check permissions
       ├── validate status
       └── ticket_repository
             └── MongoDB
```

## MongoDB Rule

MongoDB access MUST remain inside repositories.

Do not place:

```python
collection.find(...)
collection.insert_one(...)
collection.update_one(...)
```

inside FastAPI routers.

## Authentication Rule

Authentication infrastructure belongs in:

```text
app/core/security.py
app/auth/
```

Authorization decisions belong to the appropriate service/domain boundary.

## Future Evolution

The modular boundaries are intentionally designed so that a module can later be extracted into a service if necessary.

For v1, no microservices are introduced.
EOF

# --------------------------------------------------

# Development architecture guide

# --------------------------------------------------

cat > docs/development.md <<'EOF'

# Development Guidelines

## Project Commands

Install dependencies:

```bash
uv sync
```

Run the API:

```bash
uv run uvicorn app.main:app --reload
```

Run tests:

```bash
uv run pytest
```

Lint:

```bash
uv run ruff check .
```

Format:

```bash
uv run ruff format .
```

Type checking:

```bash
uv run mypy app
```

## Module Rule

New business functionality should be placed in the appropriate module.

Example:

```text
tickets/
├── router.py
├── schemas.py
├── service.py
└── repository.py
```

Do not create generic folders such as:

```text
app/
├── models/
├── controllers/
├── handlers/
└── utils/
```

unless there is a clear architectural reason.

## Testing

Tests should follow the application modules:

```text
tests/
├── auth/
├── users/
├── tickets/
├── comments/
└── attachments/
```

## Code Quality

Use:

* Type hints
* Small functions
* Explicit dependencies
* Pydantic validation
* Async MongoDB operations
* Dependency injection

Avoid:

* Global mutable state
* Business logic in routers
* Database queries in routers
* Large service classes
* Generic "utils" dumping grounds
  EOF

# --------------------------------------------------

# Architecture test

# --------------------------------------------------

cat > tests/test_architecture.py <<'EOF'
from pathlib import Path

def test_required_modules_exist():
required_modules = [
"auth",
"users",
"tickets",
"comments",
"attachments",
"health",
]

```
for module in required_modules:
    module_path = Path("app") / module

    assert module_path.is_dir()
    assert (module_path / "router.py").exists() or module == "health"
```

def test_core_and_common_exist():
assert Path("app/core").is_dir()
assert Path("app/common").is_dir()
EOF

# --------------------------------------------------

# Ruff configuration

# --------------------------------------------------

if ! grep -q "[tool.ruff]" pyproject.toml; then
cat >> pyproject.toml <<'EOF'

[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
EOF
fi

# --------------------------------------------------

# Format and lint

# --------------------------------------------------

echo
echo "Formatting application..."

uv run ruff format app tests

echo
echo "Running lint..."

uv run ruff check app tests

# --------------------------------------------------

# Tests

# --------------------------------------------------

echo
echo "Running tests..."

uv run pytest

# --------------------------------------------------

# Final output

# --------------------------------------------------

echo
echo "=========================================="
echo " Phase 01 completed successfully"
echo "=========================================="
echo
echo "Architecture created:"
echo
echo "  app/core"
echo "  app/common"
echo "  app/health"
echo "  app/auth"
echo "  app/users"
echo "  app/tickets"
echo "  app/comments"
echo "  app/attachments"
echo
echo "Documentation:"
echo
echo "  docs/architecture.md"
echo "  docs/development.md"
echo
echo "Next phase:"
echo
echo "  Phase 02 - MongoDB Foundation"
echo


SCRIPT_EOF