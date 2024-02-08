import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)
from aiogram_calendar import DialogCalendar, DialogCalendarCallback

from src.api.analysis import ideal_data
from src.api.dbapi import childapi, scheduleapi
from src.bot.filters.time import TimeFilter
from src.bot.handlers.register import router
from src.bot.handlers.register.fsm import RegisterGroup
from src.bot.handlers.register.helpers import register_user_and_child
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.bot.keyboards.register import (
    CHILD_GENDER_KEYBOARD,
    SEND_PHONE_KEYBOARD,
    get_calendar_keyboard,
)
from src.config import conf
from src.locales.ru import TEXT
from src.utils.differences import calculate_minutes_difference


@router.message(F.text == "Начать регистрацию", RegisterGroup.confirmation)
async def register_confirmation(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(user_name=message.from_user.full_name)
    await state.set_state(RegisterGroup.user_phone)
    await message.answer(TEXT["ru"]["ask_user_phone"], reply_markup=SEND_PHONE_KEYBOARD)


@router.message(
    RegisterGroup.user_phone,
    F.contact,
)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.contact.phone_number)
    await state.set_state(RegisterGroup.user_email)
    await message.answer(
        TEXT["ru"]["ask_user_email"], reply_markup=ReplyKeyboardRemove()
    )


@router.message(
    RegisterGroup.user_email,
    F.text.regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
)
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    await state.set_state(RegisterGroup.user_problem)
    await message.answer(TEXT["ru"]["ask_problem"])


@router.message(RegisterGroup.user_problem)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(RegisterGroup.child_name)
    await message.answer(TEXT["ru"]["ask_child_name"])


@router.message(RegisterGroup.child_name)
async def child_name(message: Message, state: FSMContext):
    await state.update_data(child_name=message.text)
    await state.set_state(RegisterGroup.child_birth_date)
    await message.answer(
        TEXT["ru"]["ask_child_age"],
        reply_markup=await get_calendar_keyboard(),
    )


@router.callback_query(DialogCalendarCallback.filter())
async def process_child_birth_date(
    callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    selected, date = await DialogCalendar(locale=conf.locale).process_selection(
        callback_query, callback_data
    )
    if selected:
        if date.astimezone(pytz.timezone("Etc/GMT-3")) > datetime.now(
            pytz.timezone("Etc/GMT-3")
        ):
            await callback_query.message.edit_text(
                "Нельзя выбрать будущую дату ❌. Выберите другую дату.",
                reply_markup=await get_calendar_keyboard(),
            )
        else:
            await state.update_data(child_birth_date=date)
            await state.set_state(RegisterGroup.child_gender)
            await callback_query.message.edit_text(
                "Выбранная дата: {}".format(date.strftime("%d.%m.%Y"))
            )
            await callback_query.message.answer(
                TEXT["ru"]["ask_child_gender"], reply_markup=CHILD_GENDER_KEYBOARD
            )


@router.callback_query(RegisterGroup.child_gender, F.data.in_(["male", "female"]))
async def child_gender(call: CallbackQuery, state: FSMContext):
    await state.update_data(child_gender=call.data)
    await state.set_state(RegisterGroup.food_type)
    await call.message.edit_text(TEXT["ru"]["ask_food_type"])
    await call.answer()


@router.message(RegisterGroup.food_type)
async def food_type(message: Message, state: FSMContext):
    await state.update_data(food_type=message.text)
    data = await state.get_data()
    register_user_and_child(data)
    await state.set_state(RegisterGroup.start_night_time)
    await message.answer(
        "Регистрация прошла успешно!\nТеперь для точности статистики мне нужно узнать информацию по прошедшей ночи."
    )
    await message.answer("Во сколько вы уснули вчера ночью?")


@router.message(RegisterGroup.start_night_time, TimeFilter())
async def start_night_time(message: Message, state: FSMContext):
    await state.update_data(start_night_time=message.text)
    await state.set_state(RegisterGroup.end_night_time)
    await message.answer(
        "Во сколько вы проснулись сегодня утром?\n\n<i>Если сейчас утро и ребёнок еще не проснулся, то дождитесь когда он проснётся и напишите время</i>"
    )


@router.message(RegisterGroup.end_night_time, TimeFilter())
async def end_night_time(message: Message, state: FSMContext):
    await state.update_data(end_night_time=message.text)
    data = await state.get_data()
    end_night_time = data.get("end_night_time")
    start_prev_night = data.get("start_night_time")
    current_date = datetime.now(pytz.timezone("Etc/GMT-3")).strftime("%Y-%m-%d")
    end_night_time = datetime.strptime(
        f"{current_date} {end_night_time}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=pytz.timezone("Etc/GMT-3"))
    current_time = datetime.now(pytz.timezone("Etc/GMT-3"))
    child_age = childapi.read(user_id=message.from_user.id)["age"]

    ideal_time = ideal_data.ideal_data[child_age]["day"]["activity"]["average_duration"]

    ideal_time_left = ideal_time[0]
    ideal_time_right = ideal_time[1]

    next_sleep_start_left = end_night_time + timedelta(minutes=ideal_time_left)
    next_sleep_start_right = end_night_time + timedelta(minutes=ideal_time_right)
    next_sleep_delta = next_sleep_start_right - current_time
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Записать еще один сон", callback_data="day_sleep"
                )
            ]
        ]
    )

    if current_time < end_night_time:
        await message.answer("Вы указали будущее время, так нельзя))))")
    else:
        scheduleapi.create(
            user_id=message.from_user.id,
            date=current_date,
            start_day=end_night_time.strftime("%H:%M:%S"),
            start_prev_night=start_prev_night + ":00",
            night_duration=calculate_minutes_difference(
                start_prev_night + ":00", end_night_time.strftime("%H:%M:%S")
            ),
            night_rating=10,
        )
        await state.clear()
        await message.answer(
            "Информация по прошлой ночи записана. Теперь можем начинать вести статистику по сегоднящнему дню.\n\n<i>Так же вы в любой момент можете посмотреть статистику за сегоднящний день с помощью команды /stats или вызвать клавиатуру с помощью команды /menu</i>"
        )
        if current_time > next_sleep_start_right:
            await message.answer(
                f"Вы проснулись в {end_night_time.strftime('%H:%M')} утра. Для точности статистики, отметьте, пожалуйста <b>прошедшие</b> дневные сны",
                reply_markup=keyboard,
            )
        else:
            await message.answer(
                f"Вы проснулись в {end_night_time.strftime('%H:%M')} утра. Следующий ваш сон должен начаться примерно в {next_sleep_start_left.strftime('%H:%M')} - {next_sleep_start_right.strftime('%H:%M')}\n<i>Я пришлю вам напоминание, когда придет время засыпать</i>",
                reply_markup=ReplyKeyboardRemove(),
            )
            await asyncio.sleep(next_sleep_delta.seconds)
            await message.answer("Уснули?", reply_markup=MENU_KEYBOARD)


# -------------------------------------------------------------

# @router.message(RegisterGroup.child_birth_date)
# async def wrong_child_birth_date(message: Message):
#     await message.answer(
#         "Выберите дату с помощью клавиатуры",
#         reply_markup=get_calendar_keyboard(),
#     )

# @router.message(RegisterGroup.user_phone)
# async def wrong_user_phone(message: Message):
#     await message.answer("Пожалуйста, поделитесь своим номером с помощью кнопки ниже ⬇️")


# @router.message(RegisterGroup.user_email)
# async def wrong_user_email(message: Message):
#     await message.answer("Пожалуйста, введите корректный адрес электронной почты")
