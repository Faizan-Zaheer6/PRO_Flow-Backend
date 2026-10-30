# 🚀 ProFlow Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00.svg?style=flat&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-AsyncPG-4169E1.svg?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Caching-DC382D.svg?style=flat&logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?style=flat&logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ProFlow is a high-performance, enterprise-grade **asynchronous backend service** built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL (via asyncpg)**, and **Redis**. Designed with clean, layered architecture principles to handle high-concurrency workflows, scalable database operations, JWT-based authentication, and robust caching.

---

## 🛠️ Tech Stack & Infrastructure

| Layer | Technology |
|:---|:---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) — Async web framework |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) with standard extras |
| **Database ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) with AsyncIO + `asyncpg` |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) — version-controlled schema management |
| **Caching** | [Redis](https://redis.io/) — in-memory caching & rate limiting |
| **Containerization** | [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings` |
| **Authentication** | `python-jose` (JWT tokens) & `passlib` (bcrypt hashing) |
| **File Uploads** | `python-multipart` |

---

## 🌟 Key Features & Architecture

- **⚡ Fully Asynchronous:** Non-blocking I/O from HTTP layer all the way to the database using `asyncpg` and SQLAlchemy 2.0 `async_sessionmaker`.
- **🏗️ Clean Layered Architecture:** Clear separation of concerns across well-defined layers:
  - `app/api/` — API Routers and HTTP endpoint controllers
  - `app/core/` — Application configuration, environment settings, and security utilities
  - `app/db/` — Database engine initialization and async session management
  - `app/models/` — SQLAlchemy ORM models (e.g., User)
  - `app/schemas/` — Pydantic models for request validation & response serialization
  - `app/services/` — Business logic & database operations (service layer)
- **🛡️ Secure by Design:** JWT-based authentication with bcrypt password hashing, environment-driven secrets.
- **🔄 Schema Migrations:** Alembic handles all DB schema changes in a version-controlled, reproducible way.
- **🐳 Container-Ready:** Docker Compose orchestrates the API server and Redis side-by-side for a one-command startup.
- **📦 Config Driven:** All sensitive settings (DB URL, Redis, secret keys) are managed via `.env` and `pydantic-settings`.

---

## 📂 Project Structure

```text
proflow_backend/
├── alembic/                  # Alembic migration environment & scripts
│   ├── versions/             # Auto-generated migration files
│   └── env.py                # Alembic async migration setup
├── app/                      # Main application package
│   ├── api/                  # Route handlers & endpoint definitions
│   ├── core/                 # Config, settings (pydantic-settings) & security
│   ├── db/                   # Async engine & session factory
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Business logic & DB operations
│   └── main.py               # FastAPI app entry point
├── .env                      # Environment variables (not committed)
├── .gitignore                # Git ignore rules
├── alembic.ini               # Alembic configuration file
├── Dockerfile                # Docker container build specification
├── docker-compose.yml        # Multi-service orchestration (API + Redis)
└── requirements.txt          # Python package dependencies
```

---

## 🚀 Getting Started

### Prerequisites

Before running ProFlow locally, make sure you have the following installed:

- **Python** `3.10+`
- **Docker & Docker Compose** (for containerized setup)
- **PostgreSQL** instance or a managed DB like [Neon](https://neon.tech/)
- **Redis** instance or use the Docker Compose-bundled one

---

### ⚙️ Environment Configuration

Create a `.env` file in the `proflow_backend/` root directory:

```env
APP_NAME=ProFlow
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>/<dbname>?ssl=require
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_super_secret_key_here
```

> **Note:** Never commit your `.env` file. It is already included in `.gitignore`.

---

### 💻 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Faizan-Zaheer6/PRO_Flow-Backend.git
   cd proflow_backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file** (see [Environment Configuration](#️-environment-configuration) above).

5. **Run Alembic database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`.

---

### 🐳 Running with Docker Compose

Spin up the full stack (API + Redis) in a single command:

```bash
docker-compose up --build
```

To run in detached mode:

```bash
docker-compose up --build -d
```

To stop all services:

```bash
docker-compose down
```

The API will be accessible at `http://localhost:8000`.

---

## 📌 API Endpoints & Interactive Docs

Once the server is running, explore the auto-generated interactive documentation:

| Tool | URL |
|:---|:---|
| **Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

### Core Endpoints

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/` | Root welcome message |
| `GET` | `/health` | Application health check status |

---

## 🔐 Authentication

ProFlow uses **JWT (JSON Web Tokens)** for stateless authentication:

- Passwords are hashed using **bcrypt** via `passlib`.
- Tokens are signed and verified using `python-jose`.
- Secrets are loaded securely from environment variables.

---

## 🧪 Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback the last migration
alembic downgrade -1

# Auto-generate a new migration after model changes
alembic revision --autogenerate -m "your migration message"
```

---

## 📦 Dependencies

```
fastapi
uvicorn[standard]
sqlalchemy[asyncio]
asyncpg
alembic
pydantic[email]
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-multipart
redis
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Faizan Zaheer**
- GitHub: [@Faizan-Zaheer6](https://github.com/Faizan-Zaheer6)
- Repository: [PRO_Flow-Backend](https://github.com/Faizan-Zaheer6/PRO_Flow-Backend)
