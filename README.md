# backend-service

A minimal FastAPI CRUD showcase: an `Item` resource backed by an in-memory store.
No database, no external services — just FastAPI, Pydantic, and pytest.

## Features

- Full CRUD for `/items` (create, list, get, update, delete)
- Request/response validation via Pydantic models
- Auto-generated interactive docs (Swagger UI / ReDoc)
- Test suite using FastAPI's `TestClient`

## Requirements

- Python 3.11+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Run the app

```bash
uvicorn app.main:app --reload
```

Then visit:

- http://127.0.0.1:8000/docs — Swagger UI
- http://127.0.0.1:8000/redoc — ReDoc

## Run the tests

```bash
pytest
```

## Run with Docker

```bash
docker build -t backend-service .
docker run --rm -p 8000:8000 backend-service
```

Then visit http://127.0.0.1:8000/docs as above.

## API

| Method | Path          | Description        |
|--------|---------------|---------------------|
| GET    | `/items`      | List all items      |
| POST   | `/items`      | Create an item      |
| GET    | `/items/{id}` | Get a single item   |
| PUT    | `/items/{id}` | Update an item      |
| DELETE | `/items/{id}` | Delete an item      |

### Item schema

```json
{
  "id": 1,
  "name": "Widget",
  "description": "A useful widget",
  "price": 9.99,
  "quantity": 5
}
```

## Notes

The item store is a plain in-memory dictionary (`app/store.py`), so all data is lost when the
process restarts. This is intentional — the goal of this project is to demonstrate FastAPI's
CRUD and validation capabilities, not to be a production-ready service.
