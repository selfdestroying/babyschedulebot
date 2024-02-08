from datetime import datetime

import pytz
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from src.api.dbapi import scheduleapi
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.utils.differences import calculate_minutes_difference

router = Router()


class Day(StatesGroup):
    fall_asleep_time = State()
    wake_up_time = State()


@router.message(StateFilter(None), F.text == "Отметить время дневного сна ☀️")
@router.callback_query(F.data == "day_sleep")
async def day_sleep_time(message: Message, state: FSMContext):
    id = message.from_user.id
    current_date = datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y-%m-%d")
    schedule = scheduleapi.read(user_id=id, date=current_date)
    if schedule:
        await state.update_data(id=id)
        await state.update_data(date=current_date)
        await state.set_state(Day.fall_asleep_time)
        await message.answer(
            "Когда вы уснули днем? (Введите время в формате ЧЧ:ММ)",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Нет данных про ночной сон. Пожалуйста сначала отметьте начало и конец ночного сна",
            reply_markup=MENU_KEYBOARD,
        )


@router.message(
    Day.fall_asleep_time,
    F.text.regexp(r"^\d{2}:\d{2}$"),
)
async def fall_asleep_time(message: Message, state: FSMContext):
    await state.update_data(fall_asleep_time=message.text)
    await state.set_state(Day.wake_up_time)
    await message.answer("Когда вы проснулись днем? (Введите время в формате ЧЧ:ММ)")


@router.message(
    Day.wake_up_time,
    F.text.regexp(r"^\d{2}:\d{2}$"),
)
async def wake_up_time(message: Message, state: FSMContext):
    await state.update_data(wake_up_time=message.text)
    data = await state.get_data()
    id = data.get("id")
    date = data.get("date")
    fall_asleep_time = data.get("fall_asleep_time") + ":00"
    wake_up_time = data.get("wake_up_time") + ":00"
    total_minutes = calculate_minutes_difference(fall_asleep_time, wake_up_time)
    scheduleapi.update_sleeps(
        user_id=id,
        date=date,
        sleep={
            "start_sleep_time": fall_asleep_time,
            "end_sleep_time": wake_up_time,
            "sleep_duration": total_minutes,
        },
    )
    await message.answer(f"Вы спали {total_minutes} минут", reply_markup=MENU_KEYBOARD)
    await state.clear()


@router.message(Day.fall_asleep_time, F.text)
@router.message(Day.wake_up_time, F.text)
async def wrong_time_answer(message: Message):
    await message.answer("Неправильный формат времени. Введите время в формате ЧЧ:ММ")
