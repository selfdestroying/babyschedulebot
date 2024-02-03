import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import day, info, menu, night, registration, stats

load_dotenv()
TOKEN = os.environ["BOT_TOKEN"]


async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(
        registration.router,
        info.router,
        stats.router,
        night.router,
        day.router,
        menu.router,
    )

    # Scheduled sending messages
    # async def tick():
    #     with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
    #         user_data = json.load(json_file)
    #         for id in user_data.keys():
    #             await bot.send_message(chat_id=id, text="Tick")

    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(tick, trigger="cron", minute="*/1")
    # scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
