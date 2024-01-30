from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from db.schedule import add_sleep
from models.Sleep import Sleep
from utils.utils import calculate_time_difference

router = Router()


class Day(StatesGroup):
    fall_asleep_time = State()
    wake_up_time = State()


@router.message(StateFilter(None), F.text.lower() == "отметить время дневного сна ☀️")
async def day_sleep_time(message: Message, state: FSMContext):
    data = await state.get_data()
    if "activity_count" not in data:
        i = 1
        await state.update_data(activity_count=i)
    else:
        i = data["activity_count"]
    await message.answer("Когда вы уснули днем? (Введите время в формате ЧЧ:ММ)")
    await state.set_state(Day.fall_asleep_time)


# TODO: Add time validation
@router.message(Day.fall_asleep_time)
async def fall_asleep_time(message: Message, state: FSMContext):
    await state.update_data(fall_asleep_time=message.text)
    await message.answer("Когда вы проснулись днем? (Введите время в формате ЧЧ:ММ)")
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
    try:
        add_sleep(str(message.from_user.id), sleep_data)
        await message.answer(f"Вы спали {total_minutes} минут")
    except KeyError:
        await message.answer(
            "Нет данных про ночной сон. Пожалуйста отметьте начало и конец ночного сна"
        )
    await state.clear()
