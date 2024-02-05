from aiogram import F, Router
from aiogram.types import Message

from src.api.dbapi import childapi, userapi
from src.bot.handlers.night import Night

router = Router()


@router.message(F.text == "Профиль 👥")
@router.message(Night.start_night_sleep_time, F.text == "Профиль 👥")
@router.message(Night.end_night_sleep_time, F.text == "Профиль 👥")
async def info(message: Message):
    id = message.from_user.id
    user = userapi.read(id)
    child = childapi.read(id)
    name = user["name"]
    phone = user["phone"]
    email = user["email"]
    child_name = child["name"]
    child_age = child["age"]
    child_gender = "Девочка" if child["gender"] == "female" else "Мальчик"
    food_type = child["food_type"]

    html_info_text = "Информация о <b>родителе 🧑</b>\nИмя: {}\nТелефон: {}\nEmail: {}\nИнформация о <b>ребенке 👶</b>\nИмя: {}\nВозраст: {} месяцев\nПол: {}\nТип питания: {}".format(
        name, phone, email, child_name, child_age, child_gender, food_type
    )

    await message.answer(html_info_text)
