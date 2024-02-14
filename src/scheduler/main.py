from aiogram import Bot

from src.config import conf


async def startup(ctx):
    ctx["bot"] = Bot(token=conf.bot.token)


async def shutdown(ctx):
    await ctx["bot"].session.close()


async def send_message(ctx, chat_id: int, text: str):
    bot: Bot = ctx["bot"]
    await bot.send_message(chat_id=chat_id, text=text)


class WorkerSettings:
    redis_settings = conf.redis.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_message]
    allow_abort_jobs = True
