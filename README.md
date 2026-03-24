# Order Tracking System

Track the status of orders using a 13-digit item number.

## Architecture

```
                 ┌──────────────┐
  User ────────▶ │  API Gateway │ :8080
                 │   (Nginx)    │
                 └──┬────┬────┬─┘
                    │    │    │
            /api/*  │ /* │    │ /otlp/*
                    ▼    ▼    │
             ┌──────────┐ ┌──────────┐  │
             │ Backend  │ │ Frontend │  │
             │ (FastAPI)│ │ (React)  │  │
             └──┬──┬──┬─┘ └──────────┘  │
                │  │  │                  │
                ▼  │  ▼                  ▼
         ┌───────┐ │ ┌────────┐   ┌───────────┐
         │ Redis │ │ │Postgres│   │  Jaeger   │
         │ Cache │ │ │  DB    │   │ (Tracing) │
         └───────┘ │ └────────┘   └───────────┘
                   │      OTLP/gRPC    ▲
                   └───────────────────┘
```

## Services

| Service       | Tech             | Port  |
|---------------|------------------|-------|
| API Gateway   | Nginx            | 8080  |
| Backend       | Python / FastAPI | 8000  |
| Frontend      | React 18         | 3000  |
| Database      | PostgreSQL 16    | 5432  |
| Cache         | Redis 7          | 6379  |
| Jaeger        | Jaeger 2.4       | 16686 |

## Quick Start

```bash
docker compose up --build
```

Open http://localhost:8080

## Migrate Data to Redis Cache

Pre-load all tracking data from PostgreSQL into Redis:

```bash
docker compose exec backend python -m migrate.migrate_data
```

## API Endpoints

| Method | Endpoint               | Description                          |
|--------|------------------------|--------------------------------------|
| POST   | `/api/track`           | Track multiple items (JSON body)     |
| GET    | `/api/track/{item_number}` | Track a single item              |
| GET    | `/api/track/batch/`    | Track multiple items (query params)  |

### Examples

**Single item:**
```bash
curl http://localhost:8080/api/track/EF582568151TH
```

**Batch (POST):**
```bash
curl -X POST http://localhost:8080/api/track \
  -H 'Content-Type: application/json' \
  -d '{"item_numbers": ["EF582568151TH", "EA666458151TH"]}'
```

## Sample Item Numbers

- EF582568151TH
- EA666458151TH
- RG453678925TH
- EF582621151TH
- AB123456789TH

## Distributed Tracing with Jaeger

This project uses **OpenTelemetry** to collect distributed traces and **Jaeger** as the tracing backend. Traces flow from the frontend through the API gateway to the backend and its downstream dependencies (PostgreSQL, Redis).

### How It Works

| Layer    | Instrumentation | Protocol | Destination |
|----------|----------------|----------|-------------|
| Frontend | OpenTelemetry SDK for Web (Fetch) | OTLP/HTTP | Jaeger via Nginx (`/otlp/`) |
| Backend  | OpenTelemetry SDK for Python (FastAPI, SQLAlchemy, Redis) | OTLP/gRPC | Jaeger (:4317) |

- **Frontend** traces are sent over HTTP to the API Gateway at `/otlp/v1/traces`, which proxies them to Jaeger's OTLP HTTP receiver (port 4318).
- **Backend** traces are sent directly to Jaeger via OTLP/gRPC (port 4317). FastAPI requests, SQLAlchemy queries, and Redis commands are all auto-instrumented.

### Viewing Traces

Open the Jaeger UI:

```
http://localhost:16686
```

Select service `tracking-backend` or `tracking-frontend` to explore traces.

### Service Names

| Service | `service.name` |
|---------|----------------|
| Backend | `tracking-backend` |
| Frontend | `tracking-frontend` |

## Project Structure

```
├── backend/          # FastAPI backend + Redis caching + OTel tracing
│   ├── app/          # Application code (main, models, schemas, crud, cache, tracing)
│   ├── migrate/      # Data migration scripts
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React frontend + OTel browser tracing
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── api-gateway/      # Nginx reverse proxy (proxies /otlp/ to Jaeger)
│   ├── nginx.conf
│   └── Dockerfile
├── database/         # PostgreSQL init scripts
│   └── init.sql
└── docker-compose.yml
```
