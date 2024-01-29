import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import day, info, menu, night, registration

TOKEN = os.getenv("BOT_TOKEN")


#     child_text = f"Имя ребенка: {html.quote(child_name)}\nПол ребенка: {child_gender}\nВозраст ребенка: {child_age}\nТип питания: {foodtype}"
#     user_text = f"Имя родителя: {name}\nТелефон: {phone}\nEmail: {email}"
#     await message.answer(text=user_text)
#     await message.answer(text=child_text)


async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(
        menu.router, info.router, registration.router, night.router, day.router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
