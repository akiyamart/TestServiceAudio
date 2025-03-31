from redis import asyncio as aioredis

from ..config.settings import settings
from .logger import logger

class RedisConnectionManager:
    _redis = None

    async def get_redis_connection(self):
        if self._redis is None:
            await logger.write("Starting Redis Application")
            self._redis = await aioredis.from_url(settings.REDIS_DSN, max_connections=10)
        await logger.write(f"Redis {self._redis}")
        return self._redis

redis_connection = RedisConnectionManager()


