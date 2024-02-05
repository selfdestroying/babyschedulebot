from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отметить время дневного сна ☀️")],
        [KeyboardButton(text="Отметить начало ночного сна 🌃")],
        [KeyboardButton(text="Статистика 📊"), KeyboardButton(text="Профиль 👥")],
    ],
    resize_keyboard=True,
)
