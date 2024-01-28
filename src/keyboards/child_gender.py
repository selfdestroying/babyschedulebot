from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_child_gender_kb() -> InlineKeyboardMarkup:
    male_btn = InlineKeyboardButton(text="Мальчик", callback_data="male")
    female_btn = InlineKeyboardButton(text="Девочка", callback_data="female")
    child_gender_kb = InlineKeyboardBuilder().add(male_btn, female_btn)
    return child_gender_kb.as_markup(resize_keyboard=True)
