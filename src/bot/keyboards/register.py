from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram_calendar import DialogCalendar

REGISTER_START_CONFIRM = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Начать регистрацию")]], resize_keyboard=True
)
CHILD_GENDER_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мальчик", callback_data="male")],
        [InlineKeyboardButton(text="Девочка", callback_data="female")],
    ]
)

SEND_PHONE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def get_calendar_keyboard():
    return await DialogCalendar(locale="ru_RU").start_calendar()
