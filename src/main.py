import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import registration, menu, night, day

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)


# @main_router.message(UserData.main_menu)
# async def main_menu(message: Message, state: FSMContext):
#     await message.answer("Вы в главном меню. Выберите нужную команду при помощи кнопки")


# async def show_summary(message: Message, data: dict) -> None:
#     with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
#         user_data = json.load(json_file)
#     with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
#         user_data[message.from_user.id] = {"personal_info": data, "schedule": {}}
#         json.dump(user_data, json_file, ensure_ascii=False, indent=4)
#     name = data.get("name")
#     phone = data.get("user_phone")
#     email = data.get("user_email")
#     child_name = data.get("child_name")
#     child_gender = data.get("child_gender")
#     child_age = data.get("child_age")
#     foodtype = data.get("foodtype")
#     child_text = f"Имя ребенка: {html.quote(child_name)}\nПол ребенка: {child_gender}\nВозраст ребенка: {child_age}\nТип питания: {foodtype}"
#     user_text = f"Имя родителя: {name}\nТелефон: {phone}\nEmail: {email}"
#     await message.answer(text=user_text)
#     await message.answer(text=child_text)


async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(menu.router, registration.router, night.router, day.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
