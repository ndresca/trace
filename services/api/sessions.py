"""Session persistence: Redis-backed with in-memory fallback."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)

SESSION_TTL = 86400  # 24 hours


def _serialize(session: dict) -> str:
    """Convert session dict to JSON. Sets become lists for serialization."""
    out = {}
    for key, value in session.items():
        if isinstance(value, set):
            out[key] = {"__set__": list(value)}
        else:
            out[key] = value
    return json.dumps(out)


def _deserialize(raw: str) -> dict:
    """Convert JSON back to session dict. Restores sets."""
    data = json.loads(raw)
    out = {}
    for key, value in data.items():
        if isinstance(value, dict) and "__set__" in value:
            out[key] = set(value["__set__"])
        else:
            out[key] = value
    return out


class SessionStore:
    """Abstracts session storage. Uses Redis if available, in-memory otherwise."""

    def __init__(self) -> None:
        self._redis = None
        self._memory: dict[str, dict] = {}
        self._using_redis = False

        redis_url = os.environ.get("REDIS_URL")
        if redis_url:
            try:
                import redis
                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()
                self._using_redis = True
                logger.info("Session store: Redis connected (%s)", redis_url[:30] + "...")
            except Exception as e:
                logger.warning("Session store: Redis unavailable (%s), falling back to in-memory", e)
                self._redis = None
        else:
            logger.info("Session store: No REDIS_URL set, using in-memory sessions")

    @property
    def backend(self) -> str:
        return "redis" if self._using_redis else "memory"

    def get(self, session_id: str) -> Optional[dict]:
        if self._using_redis:
            try:
                raw = self._redis.get(f"session:{session_id}")
                if raw is None:
                    return None
                return _deserialize(raw)
            except Exception as e:
                logger.warning("Redis get failed (%s), trying memory fallback", e)
                return self._memory.get(session_id)
        return self._memory.get(session_id)

    def set(self, session_id: str, session: dict) -> None:
        if self._using_redis:
            try:
                self._redis.setex(f"session:{session_id}", SESSION_TTL, _serialize(session))
                return
            except Exception as e:
                logger.warning("Redis set failed (%s), falling back to memory", e)
        self._memory[session_id] = session

    def save(self, session_id: str, session: dict) -> None:
        """Alias for set — call after mutating a session."""
        self.set(session_id, session)

    def delete(self, session_id: str) -> None:
        if self._using_redis:
            try:
                self._redis.delete(f"session:{session_id}")
                return
            except Exception:
                pass
        self._memory.pop(session_id, None)

    def set_feedback(self, session_id: str, entry: dict) -> None:
        """Store feedback under a separate key with 30-day TTL."""
        if self._using_redis:
            try:
                import json
                self._redis.setex(
                    f"feedback:{session_id}",
                    30 * 86400,
                    json.dumps(entry),
                )
            except Exception as e:
                logger.warning("Redis feedback write failed: %s", e)
