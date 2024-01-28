from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_rate_kb() -> InlineKeyboardMarkup:
    rate_kb = InlineKeyboardBuilder()
    for i in range(1, 11):
        rate_kb.add(InlineKeyboardButton(text=f"{str(i)} ⭐", callback_data=str(i)))
    rate_kb.adjust(5)
    return rate_kb.as_markup()
