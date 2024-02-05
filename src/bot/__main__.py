import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.enums import ParseMode

from src.bot.dispatcher import get_dispatcher
from src.config import conf


async def main() -> None:
    bot = Bot(token=conf.bot.token, parse_mode=ParseMode.HTML)
    dp = get_dispatcher()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
