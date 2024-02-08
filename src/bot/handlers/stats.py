from aiogram import Router
from aiogram.types import Message

from src.api.analysis.analysis import get_recomendation
from src.api.dbapi import childapi, scheduleapi

router = Router()


async def show_stats(message: Message, date: str):
    id = message.from_user.id
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
