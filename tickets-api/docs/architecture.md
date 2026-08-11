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
