import redis.asyncio as redis

from core.config import cfg
from core.exceptions import exception
from redis import RedisError


class Cache:
    def __init__(self, host=cfg.redis.HOST, port=cfg.redis.PORT, db=cfg.redis.DB):
        self.host = host
        self.port = port
        self.db = db
        self.connection_pool = redis.ConnectionPool(
            host=self.host, port=self.port, db=self.db
        )
        self.redis_cache = redis.StrictRedis(connection_pool=self.connection_pool)

    async def set(self, key: str, value: str, expire: int = 60):
        try:
            await self.redis_cache.set(key, value, expire)
        except RedisError as e:
            raise exception(400, "Ошибка сохранения данных в кэш", str(e)) from e

    async def get(self, key, decode="utf-8"):
        res = await self.redis_cache.get(key)
        if res:
            return res.decode(decode)
        return res

    async def delete(self, key: str):
        await self.redis_cache.delete(key)


cache = Cache()
