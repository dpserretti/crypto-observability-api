# Crypto Observability API (Backend)

Backend service for the **Crypto Observability** project, built with **FastAPI**.
This API aggregates and exposes cryptocurrency market data (via CoinGecko) and
is designed with clean architecture, strong typing, and production-ready practices.

---

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **HTTPX** (external API client)
- **JWT Authentication**
- **Redis** (cache)
- **PostgreSQL** (optional, persistence)
- **Pytest**
- **Ruff** (linter)
- **Black** (formatter)
- **direnv** (optional, local environment automation)

---

## Project Goals

- Fetch and normalize crypto market data
- Measure external API performance (latency, errors, availability)
- Expose secure endpoints for a frontend dashboard
- Handle authentication and authorization via JWT
- Provide a clean, production-ready backend architecture

---

## Environment Setup

### Requirements

- Python **3.11+**
- `pip`
- **direnv** (optional but recommended for local development)

> ⚠️ This repository includes a **versioned `.envrc` file**.
> If you have `direnv` installed, you only need to run `direnv allow` once.

---

## Virtual Environment Management (direnv)

This project uses **direnv with `layout python3`** to automatically create,
activate, and deactivate a Python virtual environment.

The virtual environment lifecycle is handled by direnv when entering or leaving
the project directory.

The `.envrc` file is already versioned in this repository.

---

### Using direnv (Recommended)

Install direnv (Ubuntu):

```bash
sudo apt install direnv
```

Ensure the direnv hook is enabled in your shell (`.bashrc`).

After cloning the repository, run:

```bash
direnv allow
```

From this point on:

- Entering the project directory automatically creates and activates a virtual environment
- Leaving the directory automatically deactivates it
- No manual virtual environment creation is required

---

### Manual virtual environment (without direnv)

If you prefer not to use direnv, you can manage the virtual environment manually:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

> In this case, you can safely ignore the `.envrc` file.

---

## Install Dependencies

```bash
pip install -e ".[dev]"
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Interactive docs:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

---

## Linting and Formatting

```bash
ruff check .
black .
```

---

## Testing

```bash
pytest
```

---

## Git Workflow

This project follows **Conventional Commits**:

- `feat:` new features
- `fix:` bug fixes
- `chore:` tooling / maintenance
- `refactor:` code refactors
- `test:` tests only

---

## License

MIT