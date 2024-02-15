"""This file represent startup bot logic."""
import asyncio
import logging

from aiogram import Bot
from aiogram.enums import ParseMode
from arq import create_pool
from redis.asyncio import Redis

from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.config import conf


async def start_bot():
    """This function will start bot with polling mode."""
    bot = Bot(token=conf.bot.token, parse_mode=ParseMode.HTML)
    storage = get_redis_storage(
        redis=Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            username=conf.redis.username,
            port=conf.redis.port,
            password=conf.redis.passwd,
        )
    )
    redis_pool = await create_pool(conf.redis.pool_settings)
    dp = get_dispatcher(storage=storage)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        arqredis=redis_pool,
    )


if __name__ == "__main__":
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(start_bot())
