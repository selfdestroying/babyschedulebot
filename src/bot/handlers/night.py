from datetime import datetime, timedelta

import pytz
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
)
from arq import ArqRedis

from src.api.analysis.analysis import get_recomendation
from src.api.dbapi import scheduleapi
from src.bot.filters.time import TimeFilter
from src.bot.handlers.day import Day
from src.bot.handlers.menu import MenuGroup
from src.bot.handlers.register.fsm import RegisterGroup
from src.bot.keyboards.night import END_SLEEP_KEYBOARD, get_rate_kb
from src.phrases import ru

night_router = Router()


class Night(StatesGroup):
    start_night_time = State()
    day_rating = State()
    end_night_sleep_time = State()
    night_rating = State()
    middle = State()


@night_router.message(MenuGroup.menu, F.text == "Отметить начало ночного сна 🌃")
async def start_night_time(message: Message, state: FSMContext):
    data = await state.get_data()
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    await state.set_state(Night.start_night_time)
    await message.answer(ru.NIGHT_FALL_ASLEEP[child_gender].format(child_name))


@night_router.message(Night.start_night_time, TimeFilter())
async def start_night_time_answer(message: Message, state: FSMContext):
    await state.update_data(start_night_time=message.text + ":00")
    await state.set_state(Night.day_rating)
    await message.answer(ru.ASK_DAY_RATING, reply_markup=get_rate_kb())


@night_router.callback_query(
    Night.day_rating, F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
)
async def day_rating(
    callback_query: CallbackQuery, state: FSMContext, arqredis: ArqRedis
):
    await state.update_data(day_rating=callback_query.data)
    current_date = datetime.now(pytz.timezone("Etc/GMT-3"))
    data = await state.get_data()
    id = callback_query.from_user.id
    start_night_time = data.get("start_night_time")
    child_age = data.get("child_age")
    ideal_data = data.get("ideal_data_for_age")
    ideal_night_sleep = ideal_data["night"]["total"][1]

    scheduleapi.update(
        id=id,
        date=current_date.strftime("%Y-%m-%d"),
        payload={"end_day": start_night_time, "day_rating": callback_query.data},
    )
    schedule = scheduleapi.read(user_id=id, date=current_date)
    data, text = get_recomendation(child_age=child_age, schedule=schedule)
    scheduleapi.update(id, current_date, data)
    await state.set_state(Night.middle)
    await callback_query.message.answer(text, reply_markup=END_SLEEP_KEYBOARD)
    await callback_query.message.answer(ru.RECOMENDATION)
    wake_up_job_id = await arqredis.enqueue_job(
        "send_message",
        _defer_by=timedelta(minutes=ideal_night_sleep),
        chat_id=id,
        text="Проснулись?",
    )
    await state.update_data(wake_up_job_id=wake_up_job_id.job_id)
    await callback_query.answer()
    # id = message.from_user.id
    # current_date = datetime.now(pytz.timezone("Etc/GMT-3"))
    # date_str = current_date.strftime("%Y-%m-%d")
    # start_night_sleep_time = message.text + ":00"
    # next_day = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
    # prev_day = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")
    # schedule = scheduleapi.read(user_id=id, date=date_str)
    # if schedule:
    #     scheduleapi.update(
    #         id=id, date=date_str, payload={"end_day": start_night_sleep_time}
    #     )
    #     scheduleapi.create(
    #         user_id=id,
    #         date=next_day,
    #         start_day=None,
    #         start_prev_night=start_night_sleep_time,
    #         night_duration=None,
    #         night_rating=None,
    #     )
    #     await show_stats(message, date_str)
    # else:
    #     scheduleapi.update(
    #         id=id, date=prev_day, payload={"end_day": start_night_sleep_time}
    #     )
    #     scheduleapi.create(
    #         user_id=id,
    #         date=date_str,
    #         start_day=None,
    #         start_prev_night=start_night_sleep_time,
    #         night_duration=None,
    #         night_rating=None,
    #     )
    #     await show_stats(message, prev_day)
    # await state.update_data(start_night_sleep_time=start_night_sleep_time)
    # await state.set_state(Night.middle)
    # await message.answer("Отмечено начало ночного сна", reply_markup=END_SLEEP_KEYBOARD)


@night_router.message(Night.middle, F.text == "Отметить окончание ночного сна 🌅")
async def end_night_sleep_time(message: Message, state: FSMContext, arqredis: ArqRedis):
    data = await state.get_data()
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    wake_up_job_id = data.get("wake_up_job_id")
    await arqredis.delete(f"arq:job:{wake_up_job_id}")
    await state.set_state(RegisterGroup.end_night_time)
    await message.answer(ru.ASK_PREV_NIGHT_END_SLEEP[child_gender].format(child_name))


@night_router.message(
    Night.middle, F.text == "Проснулись. Это оказался не ночной сон 😔"
)
async def wrong_night_sleep(message: Message, state: FSMContext, arqredis: ArqRedis):
    data = await state.get_data()
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    wake_up_job_id = data.get("wake_up_job_id")
    await arqredis.delete(f"arq:job:{wake_up_job_id}")
    start_night_time = data.get("start_night_time")
    await state.update_data(fall_asleep_time=start_night_time)
    await state.set_state(Day.wake_up_time)
    await message.answer(ru.DAY_WAKE_UP[child_gender].format(child_name))


# @night_router.message(Night.end_night_sleep_time, TimeFilter())
# async def end_night_sleep_time_answer(message: Message, state: FSMContext):
#     await state.update_data(end_night_sleep_time=message.text)
#     await state.set_state(Night.night_rating)
#     await message.answer("Отмечено окончание ночного сна")
#     # await message.answer(TEXT["ru"]["rate"], reply_markup=get_rate_kb())


# @night_router.callback_query(
#     Night.night_rating,
#     F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
# )
# async def night_rating(call: CallbackQuery, state: FSMContext):
#     id = call.from_user.id
#     date = datetime.now(pytz.timezone("Etc/GMT-3")).strftime("%Y-%m-%d")
#     data = await state.get_data()
#     start_night_time = data["start_night_time"]
#     end_night_sleep_time = data["end_night_sleep_time"] + ":00"
#     night_duration = calculate_minutes_difference(
#         start_night_time, end_night_sleep_time
#     )
#     night_rating = int(call.data)
#     success = scheduleapi.update(
#         id=id,
#         date=date,
#         payload={
#             "start_day": end_night_sleep_time,
#             "night_duration": night_duration,
#             "night_rating": night_rating,
#         },
#     )
#     if success:
#         await state.clear()
#         await call.message.delete()
#         await call.message.answer(
#             "Спасибо за оценку! \nВаша оценка: " + str(call.data),
#             reply_markup=MENU_KEYBOARD,
#         )
#     else:
#         await state.clear()
#         await call.message.delete()
#         await call.message.answer(
#             "Вы уже отметили ночной сон за сегодняшний день!",
#             reply_markup=MENU_KEYBOARD,
#         )


@night_router.message(Night.start_night_time)
@night_router.message(Night.end_night_sleep_time)
async def wrong_time_answer(message: Message, state: FSMContext):
    await message.answer("Неправильный формат времени. Введите время в формате ЧЧ:ММ")
