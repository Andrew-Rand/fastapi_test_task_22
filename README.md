# Medical Questionnaires API  (Test)

A FastAPI backend application for retrieving medical questionnaire templates. 
Data is stored in PostgreSQL, and database migrations are managed with Alembic.

## Technologies

- Python 3.12
- FastAPI, Pydantic
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Poetry
- Docker Compose
- Pytest

## Getting Started

1. Create a `.env` file from the example:

```
cp .env.example .env
```

2. Start the application and database:

```
docker compose up --build
```

On startup, Alembic migrations are applied and the initial data is loaded from the provided JSON file.

## API

Swagger UI: http://localhost:8000/docs

OpenAPI specification: http://localhost:8000/openapi.json

Available endpoints:

[GET] `/api/v1/questionnaires` - Retrieve the list of available questionnaires
[GET] `/api/v1/questionnaires/{cod}` - Retrieve a questionnaire with answer options and grouped questions
[GET] `/health` - Check application health

The API is read-only. Available questionnaires are sorted alphabetically by name, and questions follow the order specified in the source data.

## Tests

Meke sure dev dependencies installed in poetry!

Run the tests:

```
pytest
```

or

```
poetry run pytest
```

The tests cover business logic, repository behavior, and HTTP endpoints.