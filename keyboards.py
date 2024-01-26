from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

male_btn = InlineKeyboardButton(text="Мальчик", callback_data="male")
female_btn = InlineKeyboardButton(text="Девочка", callback_data="female")
child_gender_kb = InlineKeyboardBuilder().add(male_btn, female_btn)


day_sleep_btn = KeyboardButton(text="Отметить время дневного сна ☀️")
start_night_sleep_btn = KeyboardButton(text="Отметить начало ночного сна 🌃")
end_night_sleep_btn = KeyboardButton(text="Отметить окончание ночного сна 🌅")
main_menu_kb = ReplyKeyboardBuilder()
main_menu_kb.row(day_sleep_btn)
main_menu_kb.row(start_night_sleep_btn)
main_menu_kb.row(end_night_sleep_btn)


rate_kb = InlineKeyboardBuilder()
for i in range(1, 11):
    rate_kb.add(InlineKeyboardButton(text=f"{str(i)} ⭐", callback_data=str(i)))
rate_kb.adjust(5)
