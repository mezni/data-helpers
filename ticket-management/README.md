# ticket-management

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

```bash
uv sync
```

Start MongoDB:

```bash
docker compose up -d mongodb
```

Run API:

```bash
uv run uvicorn app.main:app --reload
```

Swagger:

http://localhost:8000/api/v1/docs

ReDoc:

http://localhost:8000/api/v1/redoc

OpenAPI:

http://localhost:8000/api/v1/openapi.json

Run tests:

```bash
uv run pytest
```
