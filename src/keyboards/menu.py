from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# TODO: Maybe replace reply buttons with inline buttons?
def get_main_menu_kb() -> ReplyKeyboardMarkup:
    day_sleep_btn = KeyboardButton(text="Отметить время дневного сна ☀️")
    start_night_sleep_btn = KeyboardButton(text="Отметить начало ночного сна 🌃")
    stats_btn = KeyboardButton(text="Статистика 📊")
    info_btn = KeyboardButton(text="Информация ℹ️")
    main_menu_kb = ReplyKeyboardBuilder()
    main_menu_kb.row(day_sleep_btn)
    main_menu_kb.row(start_night_sleep_btn)
    main_menu_kb.row(stats_btn, info_btn)
    return main_menu_kb.as_markup(resize_keyboard=True)
