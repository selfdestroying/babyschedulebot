from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message

from src.api.analysis.analysis import get_recomendation
from src.api.dbapi import childapi, scheduleapi

router = Router()


@router.message(F.text == "Статистика 📊")
async def stats(message: Message):
    await message.answer(
        "Статистика за сегодня будет доступна после начала ночного сна"
    )


async def show_stats(message: Message, end_day_time: str):
    id = message.from_user.id
    date = datetime.now().strftime("%Y-%m-%d")
    schedule = scheduleapi.read(user_id=id, date=date)
    child_age = childapi.read(user_id=id)["age"]
    data, text = get_recomendation(
        child_age=child_age, schedule=schedule, end_day_time=end_day_time
    )
    scheduleapi.update(id, data)
    await message.answer(text)
