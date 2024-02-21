from redis.asyncio import Redis

from src.config import conf

redis_client = Redis(
    db=conf.redis.db,
    host=conf.redis.host,
    username=conf.redis.username,
    port=conf.redis.port,
    password=conf.redis.passwd,
)
