from datetime import datetime, timedelta

import pytz
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from arq import ArqRedis
from arq.jobs import Job

from src.api.analysis import ideal_data
from src.api.dbapi import scheduleapi
from src.bot.filters.time import TimeFilter
from src.bot.handlers.menu import MenuGroup
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.phrases import ru
from src.utils.differences import calculate_minutes_difference
from src.utils.remind import (
    calculate_time_to_remind,
    convert_minutes_to_hours_and_minutes,
)

day_router = Router()


class Day(StatesGroup):
    fall_asleep_time = State()
    wake_up_time = State()


@day_router.message(MenuGroup.menu, F.text == "Отметить время дневного сна ☀️")
async def day_sleep_time(message: Message, state: FSMContext, arqredis: ArqRedis):
    data = await state.get_data()
    print(data)
    job_id = data.get("day_fall_asleep_job_id")
    if job_id:
        await arqredis.delete(f"arq:job:{job_id}")
    child_name = data.get("child_name")
    gender = data.get("gender")
    await state.set_state(Day.fall_asleep_time)
    await message.answer(
        ru.DAY_FALL_ASLEEP[gender].format(child_name),
        reply_markup=ReplyKeyboardRemove(),
    )


@day_router.message(Day.fall_asleep_time, TimeFilter())
async def fall_asleep_time(message: Message, state: FSMContext, arqredis: ArqRedis):
    data = await state.get_data()
    child_name = data.get("child_name")
    gender = data.get("gender")
    ideal_sleep = data.get("ideal_data_for_age")["day"]["sleep"]["average_duration"]
    ideal_sleep_r = ideal_sleep[1]
    await state.update_data(fall_asleep_time=message.text + ":00")
    await state.set_state(Day.wake_up_time)
    await message.answer(ru.DAY_WAKE_UP[gender].format(child_name))
    # TODO: replace minutes from 1 to wake up time
    day_wake_up_job_id: Job = await arqredis.enqueue_job(
        "send_message",
        _defer_by=timedelta(minutes=ideal_sleep_r),
        chat_id=message.from_user.id,
        text="Проснулись?",
    )
    print(await day_wake_up_job_id.status())
    await state.update_data(day_wake_up_job_id=day_wake_up_job_id.job_id)


@day_router.message(Day.wake_up_time, TimeFilter())
async def wake_up_time(message: Message, state: FSMContext, arqredis: ArqRedis):
    await state.update_data(wake_up_time=message.text + ":00")
    data = await state.get_data()
    job_id = data.get("day_wake_up_job_id")
    await arqredis.delete(f"arq:job:{job_id}")
    id = data.get("id")
    child_name = data.get("child_name")
    gender = data.get("gender")
    age = data.get("age")
    fall_asleep_time = data.get("fall_asleep_time")
    wake_up_time = data.get("wake_up_time")
    current_date = datetime.now(pytz.timezone("Etc/GMT-3"))
    total_minutes = calculate_minutes_difference(fall_asleep_time, wake_up_time)
    scheduleapi.update_sleeps(
        user_id=id,
        date=current_date.strftime("%Y-%m-%d"),
        sleep={
            "start_sleep_time": fall_asleep_time,
            "end_sleep_time": wake_up_time,
            "sleep_duration": total_minutes,
        },
    )

    average_activity_duration = ideal_data.ideal_data[age]["day"]["activity"][
        "average_duration"
    ]
    message_send_time = current_date.strftime("%H:%M:%S")
    time_to_remind = calculate_time_to_remind(
        wake_up_time, message_send_time, average_activity_duration
    )

    if time_to_remind:
        await message.answer(
            ru.DAY_SLEEP_ANALYSIS[gender].format(
                child_name,
                convert_minutes_to_hours_and_minutes(total_minutes),
                time_to_remind["activity_duration_min"],
                time_to_remind["activity_duration_max"],
                time_to_remind["next_fall_asleep_time_min"],
                time_to_remind["next_fall_asleep_time_max"],
            )
        )
        day_fall_asleep_job_id: Job = await arqredis.enqueue_job(
            "send_message",
            _defer_by=time_to_remind["time_to_remind"],
            chat_id=id,
            text="Уснули?",
        )
        await state.update_data(day_fall_asleep_job_id=day_fall_asleep_job_id.job_id)
    await message.answer(ru.PRESS_END_DAY_SLEEP_BUTTON, reply_markup=MENU_KEYBOARD)
    await state.set_state(MenuGroup.menu)


@day_router.message(Day.fall_asleep_time, F.text)
@day_router.message(Day.wake_up_time, F.text)
async def wrong_time_answer(message: Message):
    await message.answer(ru.WRONG_TIME)
