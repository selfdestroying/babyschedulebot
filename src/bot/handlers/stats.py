from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message

from src.api.analysis.analysis import get_recomendation
from src.api.dbapi import childapi, scheduleapi
from src.bot.handlers.night import Night

router = Router()


@router.message(F.text == "Статистика 📊")
@router.message(Night.start_night_sleep_time, F.text == "Статистика 📊")
@router.message(Night.end_night_sleep_time, F.text == "Статистика 📊")
async def stats(message: Message):
    await show_stats(message)


async def show_stats(message: Message):
    id = message.from_user.id
    date = datetime.now().strftime("%Y-%m-%d")
    schedule = scheduleapi.read(user_id=id, date=date)
    child_age = childapi.read(user_id=id)["age"]
    data, text = get_recomendation(child_age=child_age, schedule=schedule)
    if data:
        scheduleapi.update(id, date, data)
        await message.answer(text)
    else:
        await message.answer(
            "Статистика за сегодня будет доступна после начала ночного сна"
        )
