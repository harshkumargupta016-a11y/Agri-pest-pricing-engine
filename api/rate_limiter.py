import logging
import os
import threading
import time

import redis
from fastapi import HTTPException, Request

logger = logging.getLogger(__name__)


class InMemoryRateLimitStore:
    """Fallback store for local/test environments where Redis is unavailable."""

    def __init__(self) -> None:
        self._data: dict[str, dict[str, float | int]] = {}
        self._lock = threading.RLock()

    def _is_expired(self, key: str) -> bool:
        entry = self._data.get(key)
        if entry is None:
            return True
        expires_at = entry.get("expires_at")
        if expires_at is None:
            return False
        return time.monotonic() >= float(expires_at)

    def get(self, key: str):
        with self._lock:
            if self._is_expired(key):
                self._data.pop(key, None)
                return None
            entry = self._data.get(key)
            return str(entry["count"]) if entry else None

    def incr(self, key: str, amount: int = 1):
        with self._lock:
            entry = self._data.setdefault(key, {"count": 0, "expires_at": 0.0})
            entry["count"] = int(entry["count"]) + amount
            if entry.get("expires_at", 0.0) == 0.0:
                entry["expires_at"] = time.monotonic() + 60
            return entry["count"]

    def expire(self, key: str, seconds: int):
        with self._lock:
            if key not in self._data:
                return True
            self._data[key]["expires_at"] = time.monotonic() + max(seconds, 0)
            return True

    def flushdb(self):
        with self._lock:
            self._data.clear()

    def pipeline(self):
        return _InMemoryPipeline(self)


class _InMemoryPipeline:
    def __init__(self, store: InMemoryRateLimitStore) -> None:
        self.store = store
        self._ops: list[tuple[str, object]] = []

    def incr(self, key: str, amount: int = 1):
        self._ops.append(("incr", (key, amount)))
        return self

    def expire(self, key: str, seconds: int):
        self._ops.append(("expire", (key, seconds)))
        return self

    def execute(self):
        results = []
        for op_name, args in self._ops:
            if op_name == "incr":
                results.append(self.store.incr(*args))
            elif op_name == "expire":
                results.append(self.store.expire(*args))
        self._ops.clear()
        return results


def _build_redis_client():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    client = redis.Redis.from_url(redis_url, decode_responses=True)
    try:
        client.ping()
        logger.info("Connected to Redis for rate limiting")
        return client
    except redis.RedisError:
        logger.warning("Redis unavailable; using in-memory rate limit fallback")
        return InMemoryRateLimitStore()


redis_client = _build_redis_client()


def verify_rate_limit(request: Request):
    """
    Distributed Rate Limiter using Redis when available and an in-memory fallback for local/test runs.
    Protects multi-core Gunicorn workers from localized DDoS and SLA degradation.
    Limit: 50 requests per minute per IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    cache_key = f"rate_limit:{client_ip}"

    try:
        current_requests = redis_client.get(cache_key)

        if current_requests and int(current_requests) >= 50:
            logger.warning(f"[Rate Limiter] SLA Protection triggered for IP: {client_ip}")
            raise HTTPException(status_code=429, detail="Too Many Requests: SLA Protection Active. Please slow down.")

        pipe = redis_client.pipeline()
        pipe.incr(cache_key, 1)
        pipe.expire(cache_key, 60)
        pipe.execute()

    except redis.RedisError as exc:
        logger.error(f"Redis rate limiter bypassed due to connection error: {exc}")
        pass
