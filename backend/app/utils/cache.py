import json
from redis.asyncio.client import Redis

from .logger import logger
from .redis import redis_connection


class Cache:
    @staticmethod
    async def add_obj(key: str, obj: str | dict, expire_minutes: int | None = None):
        redis: Redis = await redis_connection.get_redis_connection()
        value = json.dumps(obj) if isinstance(obj, dict) else obj

        if expire_minutes is not None:
            await redis.setex(name=key, time=expire_minutes * 60, value=value)
        else:
            await redis.set(name=key, value=value)
        
        await logger.write(f"Cache SET: {key} -> {value}")

    @staticmethod
    async def get_obj(key: str) -> str | dict | None:
        redis: Redis = await redis_connection.get_redis_connection()
        if response := await redis.get(key):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return response.decode()
        return None

    @staticmethod
    async def remove_obj(key: str):
        redis: Redis = await redis_connection.get_redis_connection()
        await redis.delete(key)
        await logger.write(f"Cache DEL: {key}")