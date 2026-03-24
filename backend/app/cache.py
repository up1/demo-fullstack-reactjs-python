import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def get_cached(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cached(key: str, value, ttl: int = CACHE_TTL):
    redis_client.set(key, json.dumps(value), ex=ttl)
