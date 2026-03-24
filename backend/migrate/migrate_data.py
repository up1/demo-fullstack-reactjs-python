"""
Migrate tracking data from PostgreSQL to Redis.

Reads all rows from the tracking table and populates Redis
with key format `track:{item_number}` matching the backend API cache.

Usage:
    python -m migrate.migrate_data
"""

import json
import os
import redis
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://tracking_user:tracking_pass@db:5432/tracking_db",
)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

Base = declarative_base()


class Tracking(Base):
    __tablename__ = "tracking"

    id = Column(Integer, primary_key=True)
    item_number = Column(String(13), unique=True, nullable=False)
    status = Column(String(50), nullable=False)
    location = Column(String(255))
    updated_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())


def migrate():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()

    redis_client = redis.from_url(REDIS_URL, decode_responses=True)

    rows = db.query(Tracking).all()
    count = 0
    for row in rows:
        key = f"track:{row.item_number}"
        value = {
            "item_number": row.item_number,
            "status": row.status,
            "location": row.location,
            "updated_at": row.updated_at.isoformat(),
        }
        redis_client.set(key, json.dumps(value), ex=CACHE_TTL)
        count += 1
        print(f"  Cached {key}")

    db.close()
    print(f"\nMigrated {count} items from PostgreSQL to Redis (TTL={CACHE_TTL}s)")


if __name__ == "__main__":
    migrate()
