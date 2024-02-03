from datetime import datetime

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from db.schedule import add_sleep
from db.user import get_user_by_id
from keyboards.menu import get_main_menu_kb
from models.Sleep import Sleep
from utils.differences import calculate_minutes_difference

router = Router()


class Day(StatesGroup):
    fall_asleep_time = State()
    wake_up_time = State()


@router.message(StateFilter(None), F.text.lower() == "отметить время дневного сна ☀️")
async def day_sleep_time(message: Message, state: FSMContext):
    user = get_user_by_id(str(message.from_user.id))
    current_date = datetime.now().strftime("%d.%m")
    if current_date in user.schedule:
        data = await state.get_data()
        if "activity_count" not in data:
            i = 1
            await state.update_data(activity_count=i)
        else:
            i = data["activity_count"]
        await message.answer(
            "Когда вы уснули днем? (Введите время в формате ЧЧ:ММ)",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Day.fall_asleep_time)
    else:
        await message.answer(
            "Нет данных про ночной сон. Пожалуйста отметьте начало и конец ночного сна",
            reply_markup=get_main_menu_kb(),
        )


@router.message(
    Day.fall_asleep_time,
    F.text.regexp(r"^\d{2}:\d{2}$"),
)
async def fall_asleep_time(message: Message, state: FSMContext):
    await state.update_data(fall_asleep_time=message.text)
    await message.answer("Когда вы проснулись днем? (Введите время в формате ЧЧ:ММ)")
    await state.set_state(Day.wake_up_time)


@router.message(
    Day.wake_up_time,
    F.text.regexp(r"^\d{2}:\d{2}$"),
)
async def wake_up_time(message: Message, state: FSMContext):
    fall_asleep_time = (await state.get_data())["fall_asleep_time"]
    wake_up_time = message.text
    total_minutes = calculate_minutes_difference(fall_asleep_time, wake_up_time)

    sleep_data = Sleep(
        start_sleep_time=fall_asleep_time,
        end_sleep_time=wake_up_time,
        sleep_duration=total_minutes,
    ).model_dump()
    try:
        add_sleep(str(message.from_user.id), sleep_data)
        await message.answer(
            f"Вы спали {total_minutes} минут", reply_markup=get_main_menu_kb()
        )
    except KeyError:
        await message.answer(
            "Нет данных про ночной сон. Пожалуйста отметьте начало и конец ночного сна",
            reply_markup=get_main_menu_kb(),
        )
    await state.clear()


@router.message(Day.fall_asleep_time, F.text)
@router.message(Day.wake_up_time, F.text)
async def wrong_time_answer(message: Message):
    await message.answer("Неправильный формат времени. Введите время в формате ЧЧ:ММ")
