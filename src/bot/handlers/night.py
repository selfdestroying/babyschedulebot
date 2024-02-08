from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
)

from src.api.dbapi import scheduleapi
from src.bot.filters.time import TimeFilter
from src.bot.handlers.stats import show_stats
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.bot.keyboards.night import BACK_KEYBOARD, END_SLEEP_KEYBOARD, get_rate_kb
from src.locales.ru import TEXT
from src.utils.differences import calculate_minutes_difference

router = Router()


class Night(StatesGroup):
    start_night_sleep_time = State()
    end_night_sleep_time = State()
    night_rating = State()
    middle = State()


@router.message(Night.middle, F.text)
async def end_night_sleep_time(message: Message, state: FSMContext):
    if message.text == "Отметить окончание ночного сна 🌅":
        await state.set_state(Night.end_night_sleep_time)
        await message.answer(
            "Когда вы проснулись утром? (Введите время в формате ЧЧ:ММ)"
        )
    else:
        await message.answer(
            "Нажмите на кноку чтобы отметить окончание ночного сна",
            reply_markup=END_SLEEP_KEYBOARD,
        )


@router.message(Night.start_night_sleep_time, TimeFilter())
async def start_night_sleep_time_answer(message: Message, state: FSMContext):
    id = message.from_user.id
    current_date = datetime.now()
    date_str = current_date.strftime("%Y-%m-%d")
    start_night_sleep_time = message.text + ":00"
    next_day = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
    prev_day = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")
    schedule = scheduleapi.read(user_id=id, date=date_str)
    if schedule:
        scheduleapi.update(
            id=id, date=date_str, payload={"end_day": start_night_sleep_time}
        )
        scheduleapi.create(
            user_id=id,
            date=next_day,
            start_day=None,
            start_prev_night=start_night_sleep_time,
            night_duration=None,
            night_rating=None,
        )
        await show_stats(message, date_str)
    else:
        scheduleapi.update(
            id=id, date=prev_day, payload={"end_day": start_night_sleep_time}
        )
        scheduleapi.create(
            user_id=id,
            date=date_str,
            start_day=None,
            start_prev_night=start_night_sleep_time,
            night_duration=None,
            night_rating=None,
        )
        await show_stats(message, prev_day)
    await state.update_data(start_night_sleep_time=start_night_sleep_time)
    await state.set_state(Night.middle)
    await message.answer("Отмечено начало ночного сна", reply_markup=END_SLEEP_KEYBOARD)


@router.message(Night.end_night_sleep_time, TimeFilter())
async def end_night_sleep_time_answer(message: Message, state: FSMContext):
    await state.update_data(end_night_sleep_time=message.text)
    await state.set_state(Night.night_rating)
    await message.answer("Отмечено окончание ночного сна")
    await message.answer(TEXT["ru"]["rate"], reply_markup=get_rate_kb())


@router.callback_query(
    Night.night_rating,
    F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
)
async def night_rating(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    date = datetime.now().strftime("%Y-%m-%d")
    data = await state.get_data()
    start_night_sleep_time = data["start_night_sleep_time"]
    end_night_sleep_time = data["end_night_sleep_time"] + ":00"
    night_duration = calculate_minutes_difference(
        start_night_sleep_time, end_night_sleep_time
    )
    night_rating = int(call.data)
    success = scheduleapi.update(
        id=id,
        date=date,
        payload={
            "start_day": end_night_sleep_time,
            "night_duration": night_duration,
            "night_rating": night_rating,
        },
    )
    if success:
        await state.clear()
        await call.message.delete()
        await call.message.answer(
            "Спасибо за оценку! \nВаша оценка: " + str(call.data),
            reply_markup=MENU_KEYBOARD,
        )
    else:
        await state.clear()
        await call.message.delete()
        await call.message.answer(
            "Вы уже отметили ночной сон за сегодняшний день!",
            reply_markup=MENU_KEYBOARD,
        )


@router.message(StateFilter(None), F.text == "Отметить начало ночного сна 🌃")
async def start_night_sleep_time(message: Message, state: FSMContext):
    await state.set_state(Night.start_night_sleep_time)
    await message.answer(
        "Когда вы уснули ночью? (Введите время в формате ЧЧ:ММ)",
        reply_markup=BACK_KEYBOARD,
    )


@router.message(Night.start_night_sleep_time, F.text == "Назад 🔙")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Вы в главном меню. Выберите нужную команду при помощи кнопки",
        reply_markup=MENU_KEYBOARD,
    )


@router.message(Night.start_night_sleep_time)
@router.message(Night.end_night_sleep_time)
async def wrong_time_answer(message: Message, state: FSMContext):
    await message.answer("Неправильный формат времени. Введите время в формате ЧЧ:ММ")
