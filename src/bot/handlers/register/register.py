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
from src.bot.filters.register import EmailFilter
from src.bot.filters.time import TimeFilter
from src.bot.handlers.register import router
from src.bot.handlers.register.fsm import RegisterGroup
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.bot.keyboards.register import (
    CHILD_GENDER_KEYBOARD,
    FOOD_TYPE_KEYBOARD,
    REGISTER_CONFIRM_KEYBOARD,
    SEND_PHONE_KEYBOARD,
    get_calendar_keyboard,
)
from src.config import conf
from src.phrases import ru
from src.utils.differences import (
    calculate_child_age_in_months,
    calculate_minutes_difference,
)


@router.message(RegisterGroup.user_problem, F.text)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(RegisterGroup.confirmation)
    await message.answer(ru.ABOUT_2)
    await asyncio.sleep(1)
    await message.answer(ru.REGISTER_CONFIRM, reply_markup=REGISTER_CONFIRM_KEYBOARD)


@router.message(RegisterGroup.confirmation, F.text == "Начать регистрацию")
async def register_confirmation(message: Message, state: FSMContext):
    await state.set_state(RegisterGroup.user_phone)
    await message.answer(ru.ASK_PHONE, reply_markup=SEND_PHONE_KEYBOARD)


# TODO: bug, user can share another contact
@router.message(RegisterGroup.user_phone, F.contact)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.contact.phone_number)
    await state.set_state(RegisterGroup.user_email)
    await message.answer(ru.ASK_EMAIL, reply_markup=ReplyKeyboardRemove())


@router.message(RegisterGroup.user_email, EmailFilter())
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    await state.set_state(RegisterGroup.child_name)
    await message.answer(ru.ABOUT_3)
    await asyncio.sleep(1)
    await message.answer(ru.ASK_CHILD_NAME)


@router.message(RegisterGroup.child_name, F.text)
async def child_name(message: Message, state: FSMContext):
    await state.update_data(child_name=message.text)
    await state.set_state(RegisterGroup.child_gender)
    await message.answer(ru.ASK_CHILD_GENDER, reply_markup=CHILD_GENDER_KEYBOARD)


@router.callback_query(RegisterGroup.child_gender, F.data)
async def child_gender(callback_query: CallbackQuery, state: FSMContext):
    child_gender = callback_query.data
    child_name = (await state.get_data())["child_name"]
    await state.update_data(child_gender=child_gender)
    await state.set_state(RegisterGroup.child_birth_date)
    await callback_query.message.edit_text(
        ru.ASK_CHILD_BIRTH_DATE[child_gender].format(child_name),
        reply_markup=await get_calendar_keyboard(),
    )
    await callback_query.answer()


@router.callback_query(DialogCalendarCallback.filter())
async def process_child_birth_date(
    callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    selected, date = await DialogCalendar(locale=conf.locale).process_selection(
        callback_query, callback_data
    )
    if selected:
        if date > datetime.now():
            await callback_query.message.edit_text(
                "Нельзя выбрать будущую дату ❌. Выберите другую дату.",
                reply_markup=await get_calendar_keyboard(),
            )
        else:
            date = date.strftime("%Y-%m-%d")
            child_age = calculate_child_age_in_months(date)
            await state.update_data(child_birth_date=date)
            await state.update_data(child_age=child_age)
            await state.set_state(RegisterGroup.food_type)
            await callback_query.message.answer(
                ru.ASK_FOOD_TYPE, reply_markup=FOOD_TYPE_KEYBOARD
            )


@router.callback_query(RegisterGroup.food_type, F.data)
async def food_type(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(food_type=callback_query.data)
    data = await state.get_data()
    print(data)
    # register_user_and_child(data)
    # await state.set_state(RegisterGroup.start_night_time)
    await callback_query.message.answer(ru.ABOUT_4)
    await asyncio.sleep(1)
    await callback_query.message.answer(ru.ABOUT_5)
    await asyncio.sleep(1)
    await callback_query.message.answer(ru.ABOUT_6)
    await asyncio.sleep(1)
    await callback_query.message.answer(ru.ASK_PREV_NIGHT)
    await asyncio.sleep(1)
    await callback_query.message.answer(
        ru.ASK_PREV_NIGHT_START_SLEEP[data.get("child_gender")].format(
            data.get("child_name")
        )
    )
    await callback_query.answer()


@router.message(RegisterGroup.start_night_time, TimeFilter())
async def start_night_time(message: Message, state: FSMContext):
    await state.update_data(start_night_time=message.text)
    await state.set_state(RegisterGroup.end_night_time)
    await message.answer(ru.ASK_PREV_NIGHT_END_SLEEP)


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
