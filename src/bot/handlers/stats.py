from aiogram import F, Router
from aiogram.types import Message

from src.api.analysis.analysis import get_recomendation

router = Router()


@router.message(F.text == "Статистика 📊")
async def info(message: Message):
    text = get_recomendation(str(message.from_user.id))
    await message.answer(text)
