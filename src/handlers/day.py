import datetime
import json
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db.schedule import add_sleep
from models.Sleep import Sleep

from utils.utils import calculate_time_difference

router = Router()


class Day(StatesGroup):
    fall_asleep_time = State()
    wake_up_time = State()


@router.message(F.text.lower() == "отметить время дневного сна ☀️")
async def day_sleep_time(message: Message, state: FSMContext):
    data = await state.get_data()
    if "activity_count" not in data:
        i = 1
        await state.update_data(activity_count=i)
    else:
        i = data["activity_count"]
    await message.answer(f"Когда вы уснули? (Введите время в формате ЧЧ:ММ)")
    await state.set_state(Day.fall_asleep_time)


@router.message(Day.fall_asleep_time)
async def fall_asleep_time(message: Message, state: FSMContext):
    i = (await state.get_data())["activity_count"]
    await state.update_data(fall_asleep_time=message.text)
    await message.answer(f"Когда вы проснулись? (Введите время в формате ЧЧ:ММ)")
    await state.set_state(Day.wake_up_time)


@router.message(Day.wake_up_time)
async def wake_up_time(message: Message, state: FSMContext):
    fall_asleep_time = (await state.get_data())["fall_asleep_time"]
    wake_up_time = message.text
    total_minutes = calculate_time_difference(fall_asleep_time, wake_up_time)

    sleep_data = Sleep(
        start_sleep_time=fall_asleep_time,
        end_sleep_time=wake_up_time,
        sleep_duration=total_minutes,
    ).model_dump()
    add_sleep(str(message.from_user.id), sleep_data)
    await message.answer(f"Вы спали {total_minutes} минут")
    await state.clear()