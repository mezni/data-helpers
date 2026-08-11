# Development

## Install

```bash
uv sync
```

## Start MongoDB

```bash
docker compose up -d mongodb
```

## Run API

```bash
uv run uvicorn app.main:app --reload
```

## Swagger

http://localhost:8000/api/v1/docs

## ReDoc

http://localhost:8000/api/v1/redoc

## OpenAPI

http://localhost:8000/api/v1/openapi.json

## Tests

```bash
uv run pytest
```

## Format

```bash
uv run ruff format .
```

## Lint

```bash
uv run ruff check .
```
