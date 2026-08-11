
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
