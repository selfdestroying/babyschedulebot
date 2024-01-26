import asyncio
import datetime
import json
import logging
import os
import sys

from aiogram import Bot, Dispatcher, Router, types, html, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from keyboards import child_gender_kb, main_menu_kb, rate_kb
from locales import TEXT
from utils import calculate_time_difference

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
form_router = Router()


class UserData(StatesGroup):
    name = State()
    user_problem = State()
    child_gender = State()
    child_name = State()
    child_age = State()
    foodtype = State()
    user_phone = State()
    user_email = State()
    main_menu = State()
    day_sleep_time = State()
    fall_asleep_time = State()
    wake_up_time = State()
    start_night_sleep_time = State()
    end_night_sleep_time = State()


@form_router.message(UserData.user_problem)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(UserData.child_gender)
    await message.answer(TEXT["ru"]["understand"])
    await message.answer(
        TEXT["ru"]["ask_child_gender"],
        reply_markup=child_gender_kb.as_markup(resize_keyboard=True),
    )


@form_router.callback_query(UserData.child_gender, F.data.in_(["male", "female"]))
async def child_gender(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(child_gender=call.data)
    await state.set_state(UserData.child_name)
    await call.message.edit_text(TEXT["ru"]["ask_child_name"])
    await call.answer()


@form_router.message(UserData.child_name)
async def child_name(message: Message, state: FSMContext):
    await state.update_data(child_name=message.text)
    await state.set_state(UserData.child_age)
    await message.answer(TEXT["ru"]["ask_child_age"])


@form_router.message(UserData.child_age)
async def child_age(message: Message, state: FSMContext):
    await state.update_data(child_age=message.text)
    await state.set_state(UserData.foodtype)
    await message.answer(TEXT["ru"]["ask_foodtype"])


@form_router.message(UserData.foodtype)
async def foodtype(message: Message, state: FSMContext):
    await state.update_data(foodtype=message.text)
    await state.set_state(UserData.user_phone)
    await message.answer(TEXT["ru"]["ask_user_phone"])


@form_router.message(UserData.user_phone)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.text)
    await state.set_state(UserData.user_email)
    await message.answer(TEXT["ru"]["ask_user_email"])


@form_router.message(UserData.user_email)
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    await message.answer(TEXT["ru"]["done"], reply_markup=main_menu_kb.as_markup())
    await show_summary(message, await state.get_data())
    await state.set_state(UserData.main_menu)


@form_router.message(
    UserData.main_menu, F.text.lower() == "отметить время дневного сна ☀️"
)
async def day_sleep_time(message: Message, state: FSMContext):
    data = await state.get_data()
    if "activity_count" not in data:
        i = 1
        await state.update_data(activity_count=i)
    else:
        i = data["activity_count"]
    await message.answer(f"Когда вы уснули в {i} раз? (Введите время в формате ЧЧ:ММ)")
    await state.set_state(UserData.fall_asleep_time)


@form_router.message(UserData.fall_asleep_time)
async def fall_asleep_time(message: Message, state: FSMContext):
    i = (await state.get_data())["activity_count"]
    await state.update_data(fall_asleep_time=message.text)
    await message.answer(
        f"Во сколько вы проснулись в {i} раз за день? (Введите время в формате ЧЧ:ММ)"
    )
    await state.set_state(UserData.wake_up_time)


@form_router.message(UserData.wake_up_time)
async def wake_up_time(message: Message, state: FSMContext):
    fall_asleep_time = (await state.get_data())["fall_asleep_time"]
    activity_count = (await state.get_data())["activity_count"]
    wake_up_time = message.text
    total_minutes = calculate_time_difference(fall_asleep_time, wake_up_time)
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    sleep_data = {
        "activity_count": activity_count,
        "fall_asleep_time": fall_asleep_time,
        "wake_up_time": wake_up_time,
        "sleep_duration": total_minutes,
    }
    with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
        user_data = json.load(json_file)
        id = str(message.from_user.id)
        if current_date not in user_data[id]["schedule"].keys():
            user_data[id]["schedule"][current_date] = [sleep_data]
        else:
            user_data[id]["schedule"][current_date].append(sleep_data)
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)
    await state.update_data(activity_count=activity_count + 1)
    await state.update_data(wake_up_time=wake_up_time)
    await message.answer(f"Вы спали {total_minutes} минут")
    await state.set_state(UserData.main_menu)
    await message.answer("Вы в главном меню. Выберите нужную команду при помощи кнопки")
    print(await state.get_data())


@form_router.message(
    UserData.main_menu, F.text.lower() == "отметить начало ночного сна 🌃"
)
async def start_night_sleep_time(message: Message, state: FSMContext):
    current_time = f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
    await state.update_data(start_night_sleep_time=current_time)
    await state.set_state(UserData.start_night_sleep_time)
    await message.answer("Время начала ночного сна: " + str(current_time))


@form_router.message(
    UserData.start_night_sleep_time,
    F.text.lower() == "отметить окончание ночного сна" + " 🌅",
)
async def end_night_sleep_time(message: Message, state: FSMContext):
    current_time = f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
    await state.update_data(end_night_sleep_time=current_time)
    await message.answer("Время окончания ночного сна: " + str(current_time))
    await message.answer(TEXT["ru"]["rate"], reply_markup=rate_kb.as_markup())
    await state.set_state(UserData.end_night_sleep_time)


@form_router.callback_query(
    UserData.end_night_sleep_time,
    F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
)
async def end_night_sleep_time(call: CallbackQuery, state: FSMContext):
    await state.update_data(nigth_rating=call.data)
    await call.message.edit_text("Спасибо за оценку! \nВаша оценка: " + str(call.data))
    await state.set_state(UserData.main_menu)


@form_router.message(UserData.main_menu)
async def main_menu(message: Message, state: FSMContext):
    await message.answer("Вы в главном меню. Выберите нужную команду при помощи кнопки")


async def show_summary(message: Message, data: dict) -> None:
    with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
        user_data = json.load(json_file)
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        user_data[message.from_user.id] = {"personal_info": data, "schedule": {}}
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)
    name = data.get("name")
    phone = data.get("user_phone")
    email = data.get("user_email")
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    child_age = data.get("child_age")
    foodtype = data.get("foodtype")
    child_text = f"Имя ребенка: {html.quote(child_name)}\nПол ребенка: {child_gender}\nВозраст ребенка: {child_age}\nТип питания: {foodtype}"
    user_text = f"Имя родителя: {name}\nТелефон: {phone}\nEmail: {email}"
    await message.answer(text=user_text)
    await message.answer(text=child_text)


@form_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    name = message.from_user.first_name
    id = message.from_user.id
    user_data = {}
    try:
        with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
            user_data = json.load(json_file)
    except FileNotFoundError:
        with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
            json.dump(user_data, json_file)
    finally:
        if user_data and str(id) in user_data.keys():
            print("User already exists")
            await state.set_state(UserData.main_menu)
            await message.answer(
                "Вы в главном меню. Выберите нужную команду при помощи кнопки",
                reply_markup=main_menu_kb.as_markup(resize_keyboard=True),
            )
        else:
            await state.set_state(UserData.name)
            await state.update_data(name=name)
            await message.answer(TEXT["ru"]["start"].format(hbold(name)))
            await message.answer(TEXT["ru"]["ask_problem"])
            await state.set_state(UserData.user_problem)


async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
