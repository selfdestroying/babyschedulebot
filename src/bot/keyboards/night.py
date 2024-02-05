from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

END_SLEEP_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отметить окончание ночного сна 🌅")]],
    one_time_keyboard=True,
    resize_keyboard=True,
)


def get_rate_kb() -> InlineKeyboardMarkup:
    rate_kb = InlineKeyboardBuilder()
    for i in range(1, 11):
        rate_kb.add(InlineKeyboardButton(text=f"{str(i)} ⭐", callback_data=str(i)))
    rate_kb.adjust(5)
    return rate_kb.as_markup()
