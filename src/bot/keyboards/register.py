from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram_calendar import DialogCalendar

from src.config import conf

REGISTER_CONFIRM_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Начать регистрацию")]], resize_keyboard=True
)
GENDER_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мальчик 🙋", callback_data="male")],
        [InlineKeyboardButton(text="Девочка 🙋‍♀️", callback_data="female")],
    ]
)

FOOD_TYPE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Грудь 🤱", callback_data="breast"),
        ],
        [
            InlineKeyboardButton(text="Смесь 🍼", callback_data="formula"),
        ],
        [
            InlineKeyboardButton(text="Грудь 🤱 и Смесь 🍼", callback_data="mix"),
        ],
    ]
)

SEND_PHONE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

CORRECT_ANSWER_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Исправить 🔙")]], resize_keyboard=True
)


async def get_calendar_keyboard():
    return await DialogCalendar(locale=conf.locale).start_calendar()
