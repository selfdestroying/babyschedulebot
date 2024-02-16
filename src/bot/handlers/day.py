from datetime import datetime, timedelta

import pytz
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from arq import ArqRedis
from arq.jobs import Job

from src.api.dbapi import scheduleapi
from src.bot.filters.time import TimeFilter
from src.bot.handlers.menu import MenuGroup
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.phrases import ru
from src.utils.differences import calculate_minutes_difference

day_router = Router()


class Day(StatesGroup):
    fall_asleep_time = State()
    wake_up_time = State()


@day_router.message(MenuGroup.menu, F.text == "Отметить время дневного сна ☀️")
async def day_sleep_time(message: Message, state: FSMContext, arqredis: ArqRedis):
    data = await state.get_data()
    job_id = data.get("day_fall_asleep_job_id")
    if job_id:
        await arqredis.delete(f"arq:job:{job_id}")
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    await state.set_state(Day.fall_asleep_time)
    await message.answer(
        ru.DAY_FALL_ASLEEP[child_gender].format(child_name),
        reply_markup=ReplyKeyboardRemove(),
    )


@day_router.message(Day.fall_asleep_time, TimeFilter())
async def fall_asleep_time(message: Message, state: FSMContext, arqredis: ArqRedis):
    data = await state.get_data()
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    ideal_sleep = data.get("ideal_data_for_age")["day"]["sleep"]["average_duration"]
    ideal_sleep_r = ideal_sleep[1]
    await state.update_data(fall_asleep_time=message.text + ":00")
    await state.set_state(Day.wake_up_time)
    await message.answer(ru.DAY_WAKE_UP[child_gender].format(child_name))
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
    child_gender = data.get("child_gender")
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
    wake_up_time = datetime.strptime(
        f'{current_date.strftime("%Y-%m-%d")} {wake_up_time}',
        "%Y-%m-%d %H:%M:%S",
    ).replace(tzinfo=pytz.timezone("Etc/GMT-3"))
    ideal_data_for_age = data.get("ideal_data_for_age")["day"]["activity"][
        "average_duration"
    ]

    ideal_time_left = ideal_data_for_age[0]
    ideal_time_right = ideal_data_for_age[1]

    next_sleep_start_left = wake_up_time + timedelta(minutes=ideal_time_left)
    next_sleep_start_right = wake_up_time + timedelta(minutes=ideal_time_right)
    if (current_date - wake_up_time) < timedelta(minutes=30):
        await message.answer(
            ru.DAY_SLEEP_ANALYSIS[child_gender].format(
                child_name,
                round(total_minutes / 60, 1),
                "?",
                round(ideal_time_left / 60, 1),
                round(ideal_time_right / 60, 1),
                next_sleep_start_left.strftime("%H:%M"),
                next_sleep_start_right.strftime("%H:%M"),
            )
        )
        day_fall_asleep_job_id: Job = await arqredis.enqueue_job(
            "send_message",
            _defer_by=(next_sleep_start_right - current_date).seconds,
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
