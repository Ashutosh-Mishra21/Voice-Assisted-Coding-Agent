import json
from typing import Any

import redis
from redis.exceptions import RedisError


class RedisStore:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
    ):
        self.host = host
        self.port = port
        self.db = db

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True,
        )

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except RedisError:
            return False

    def save(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        try:
            self.client.set(
                key,
                json.dumps(value),
            )
        except RedisError as e:
            raise RuntimeError(
                f"Failed to save data to Redis for key '{key}': {e}"
            ) from e

    def load(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        try:
            data = self.client.get(key)

            if not data:
                return None

            return json.loads(data)

        except RedisError as e:
            raise RuntimeError(
                f"Failed to load data from Redis for key '{key}': {e}"
            ) from e

    def delete(
        self,
        key: str,
    ) -> None:
        try:
            self.client.delete(key)
        except RedisError as e:
            raise RuntimeError(f"Failed to delete Redis key '{key}': {e}") from e
