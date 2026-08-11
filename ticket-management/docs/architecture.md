# Ticket Management API Architecture

## Architecture Style

The application is a modular monolith.

```text
Client
  |
  v
FastAPI Application
  |
  +-----------------------------+
  |          |          |        |
 Auth      Users      Tickets   Health
                       |
                +------+------+
                |      |      |
             Comments Attachments
                |
                v
             MongoDB
```

## Technology

* Python
* FastAPI
* Pydantic
* MongoDB
* uv
* Ruff
* pytest
* Swagger / OpenAPI

## Business Modules

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
```

## Module Structure

Each business module follows:

```text
module/
├── router.py
├── schemas.py
├── service.py
└── repository.py
```

## Request Flow

```text
HTTP Request
     |
     v
   Router
     |
     v
   Service
     |
     v
 Repository
     |
     v
  MongoDB
```

## Router

Routers are responsible for:

* HTTP endpoints
* Request parsing
* Response serialization
* FastAPI dependencies
* HTTP status codes

Routers must not:

* Access MongoDB directly
* Implement business rules

## Service

Services are responsible for:

* Business rules
* Workflows
* Authorization decisions
* Domain validation
* Repository coordination

Services must not depend on FastAPI request objects.

## Repository

Repositories are responsible for:

* MongoDB queries
* MongoDB writes
* Persistence operations
* MongoDB-specific implementation

Repositories must not contain HTTP logic.

## Schemas

Pydantic schemas are responsible for:

* Request validation
* Response serialization
* API contracts

## Core

`core/` contains infrastructure:

* Configuration
* MongoDB lifecycle
* Security
* Exceptions
* Logging

## Common

`common/` contains reusable infrastructure:

* API responses
* Pagination
* Shared dependencies

## Architectural Rules

1. Routers never access MongoDB directly.
2. Services contain business logic.
3. Repositories contain persistence logic.
4. Schemas contain API validation.
5. Core contains infrastructure.
6. Common contains reusable infrastructure.
7. Business modules remain isolated.
8. No microservices in v1.

## API Documentation

Swagger:

`/api/v1/docs`

ReDoc:

`/api/v1/redoc`

OpenAPI:

`/api/v1/openapi.json`
