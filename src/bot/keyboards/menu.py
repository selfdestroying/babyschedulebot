from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отметить время дневного сна ☀️")],
        [KeyboardButton(text="Отметить начало ночного сна 🌃")],
    ],
    resize_keyboard=True,
)
