# Crypto Observability API

A backend service built with FastAPI that acts as an observability layer on top of the CoinGecko API.

This service is responsible for:
- Fetching and normalizing crypto market data
- Measuring external API performance (latency, errors, availability)
- Exposing secure endpoints for a frontend dashboard
- Handling authentication and authorization via JWT

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- HTTPX (external API client)
- JWT Authentication
- Redis (cache)
- PostgreSQL (optional, for persistence)
- Pytest (tests)

---

## Architecture Overview

This project follows a layered architecture to keep concerns separated and the codebase maintainable:

app/
- api/            # HTTP layer (routes, request/response schemas)
- core/           # Application configuration and settings
- domain/         # Domain models and business rules
- services/       # Application services and use cases
- clients/        # External API clients (CoinGecko)
- infrastructure/ # Cache, database, and third-party integrations
- main.py         # FastAPI application entry point

---

## Features

- Proxy integration with the CoinGecko API
- API performance metrics (latency, status codes, error rates)
- JWT-based authentication (access and refresh tokens)
- Rate limiting and caching
- Health check endpoint
- OpenAPI documentation

---

## Getting Started

### Requirements

- Python 3.11+
- pip
- virtualenv

### Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Run the application

uvicorn app.main:app --reload

### API Docs

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

---

## Environment Variables

COINGECKO_BASE_URL=https://api.coingecko.com/api/v3
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

---

## Commit Convention

This repository follows the Conventional Commits specification:

- feat: New feature
- fix: Bug fix
- chore: Maintenance tasks
- docs: Documentation changes
- refactor: Code refactoring
- test: Adding or fixing tests

---

## License

MIT