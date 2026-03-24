# Order Tracking System

Track the status of orders using a 13-digit item number.

## Architecture

```
                 ┌──────────────┐
  User ────────▶ │  API Gateway │ :8080
                 │   (Nginx)    │
                 └──┬───────┬───┘
                    │       │
            /api/*  │       │  /*
                    ▼       ▼
             ┌─────────┐ ┌──────────┐
             │ Backend  │ │ Frontend │
             │ (FastAPI)│ │ (React)  │
             └──┬────┬──┘ └──────────┘
                │    │
                ▼    ▼
         ┌───────┐ ┌───────┐
         │ Redis │ │Postgres│
         │ Cache │ │  DB    │
         └───────┘ └───────┘
```

## Services

| Service       | Tech             | Port  |
|---------------|------------------|-------|
| API Gateway   | Nginx            | 8080  |
| Backend       | Python / FastAPI | 8000  |
| Frontend      | React 18         | 3000  |
| Database      | PostgreSQL 16    | 5432  |
| Cache         | Redis 7          | 6379  |

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

## Project Structure

```
├── backend/          # FastAPI backend + Redis caching
│   ├── app/          # Application code (main, models, schemas, crud, cache)
│   ├── migrate/      # Data migration scripts
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── api-gateway/      # Nginx reverse proxy
│   ├── nginx.conf
│   └── Dockerfile
├── database/         # PostgreSQL init scripts
│   └── init.sql
└── docker-compose.yml
```
