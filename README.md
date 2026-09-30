# 🚀 ProFlow Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00.svg?style=flat&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-AsyncPG-4169E1.svg?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Caching-DC382D.svg?style=flat&logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?style=flat&logo=docker)](https://www.docker.com/)

ProFlow is a high-performance, enterprise-grade asynchronous backend service built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL**, and **Redis**. It is designed with clean architecture principles to handle high-concurrency workflows, scalable database operations, and robust caching.

---

## 🛠️ Tech Stack & Infrastructure

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Web Framework)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Database ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (AsyncIO with `asyncpg`)
- **Database Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Cache & Rate Limiting:** [Redis](https://redis.io/)
- **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- **Configuration & Validation:** [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings`
- **Security & Authentication:** `python-jose` (JWT) & `passlib` (bcrypt)

---

## 🌟 Key Features & Architecture

- **⚡ Asynchronous I/O Performance:** Fully non-blocking database queries and request handling powered by `asyncpg` and SQLAlchemy 2.0 `async_sessionmaker`.
- **🏗️ Clean & Layered Architecture:** Clear separation of concerns:
  - `app/api`: API Routers and HTTP request controllers
  - `app/core`: Application configuration, environment settings, and security
  - `app/db`: Database engine initialization and session management
  - `app/models`: SQLAlchemy ORM database models
  - `app/schemas`: Pydantic models for request validation & response serialization
  - `app/services`: Business logic & database operations layer
- **🛡️ Security & Reliability:** JWT-based authentication infrastructure with password hashing using bcrypt.
- **🔄 Database Migrations:** Version-controlled schema migrations powered by Alembic.
- **🐳 Multi-Container Orchestration:** Containerized setup for seamless execution of API and Redis services using Docker Compose.

---

## 📂 Directory Structure

```text
proflow_backend/
├── alembic/              # Database migration scripts & environment
├── app/                  # Main application package
│   ├── api/              # API endpoints and route handlers
│   ├── core/             # App config, settings & security modules
│   ├── db/               # Database engine & async session setup
│   ├── models/           # SQLAlchemy ORM models (e.g. User model)
│   ├── schemas/          # Pydantic schemas for data validation
│   ├── services/         # Business logic layer
│   └── main.py           # FastAPI app entry point
├── .env                  # Environment variables file
├── alembic.ini           # Alembic configuration
├── Dockerfile            # Multi-stage Docker container specification
├── docker-compose.yml    # Docker Compose multi-service deployment
└── requirements.txt      # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- **Python:** `3.10+` installed locally
- **Docker & Docker Compose:** Installed for containerized execution
- **PostgreSQL / Neon DB:** Database instance URL
- **Redis:** Redis instance or Docker container

---

### ⚙️ Environment Configuration

Create a `.env` file in the root of `proflow_backend/` directory with the following variables:

```env
APP_NAME=ProFlow
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>/<dbname>?ssl=require
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_super_secret_key_here
```

---

### 💻 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Faizan-Zaheer6/Pro_Flow-Backend.git
   cd proflow_backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Alembic Migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

### 🐳 Running with Docker Compose

To start the API service alongside Redis in containerized mode:

```bash
docker-compose up --build
```

The API will be accessible at `http://localhost:8000`.

---

## 📌 API Endpoints & Interactive Documentation

Once the server is running, explore the interactive documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root welcome message |
| `GET` | `/health` | Application health check status |

---

## 📄 License

This project is open-source and available under the MIT License.

