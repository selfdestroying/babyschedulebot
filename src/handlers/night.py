from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from db.schedule import write_day_info
from keyboards.menu import get_main_menu_kb
from keyboards.rate import get_rate_kb
from locales.ru import TEXT
from models.DayInfo import DayInfo
from utils.utils import calculate_time_difference

router = Router()


class Night(StatesGroup):
    start_night_sleep_time = State()
    end_night_sleep_time = State()
    night_rating = State()


@router.message(
    Night.start_night_sleep_time, F.text.lower() == "отметить окончание ночного сна 🌅"
)
async def end_night_sleep_time(message: Message, state: FSMContext):
    await message.answer("Когда вы проснулись утром? (Введите время в формате ЧЧ:ММ)")
    await state.set_state(Night.end_night_sleep_time)


@router.message(
    Night.start_night_sleep_time,
    F.text,
    F.text.regexp(r"^\d{2}:\d{2}$"),
)
async def start_night_sleep_time_answer(message: Message, state: FSMContext):
    hours = message.text.split(":")[0]
    minutes = message.text.split(":")[1]
    if int(hours) < 0 or int(hours) > 23 or int(minutes) < 0 or int(minutes) > 59:
        await message.answer(
            "Неправильный формат времени. Введите время в формате ЧЧ:ММ"
        )
    else:
        await state.update_data(start_night_sleep_time=message.text)
        await message.answer("Отмечено начало ночного сна")


@router.message(
    Night.end_night_sleep_time,
    F.text,
    F.text.regexp(r"^\d{2}:\d{2}$"),
)
async def end_night_sleep_time_answer(message: Message, state: FSMContext):
    hours = message.text.split(":")[0]
    minutes = message.text.split(":")[1]
    if int(hours) < 0 or int(hours) > 23 or int(minutes) < 0 or int(minutes) > 59:
        await message.answer(
            "Неправильный формат времени. Введите время в формате ЧЧ:ММ"
        )
    else:
        await state.update_data(end_night_sleep_time=message.text)
        await state.set_state(Night.night_rating)
        await message.answer(
            "Отмечено окончание ночного сна", reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(TEXT["ru"]["rate"], reply_markup=get_rate_kb())


@router.message(
    Night.start_night_sleep_time,
    F.text,
)
@router.message(
    Night.end_night_sleep_time,
    F.text,
)
async def wrong_time_answer(message: Message, state: FSMContext):
    await message.answer("Неправильный формат времени. Введите время в формате ЧЧ:ММ")


@router.callback_query(
    Night.night_rating,
    F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
)
async def night_rating(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "Спасибо за оценку! \nВаша оценка: " + str(call.data),
        reply_markup=get_main_menu_kb(),
    )
    data = await state.get_data()
    start_night_sleep_time = data["start_night_sleep_time"]
    end_night_sleep_time = data["end_night_sleep_time"]
    day_info = DayInfo(
        start_night_sleep_time=start_night_sleep_time,
        end_night_sleep_time=end_night_sleep_time,
        night_duration=calculate_time_difference(
            start_night_sleep_time, end_night_sleep_time
        ),
        night_rating=call.data,
        sleeps=[],
    )
    write_day_info(id=str(call.from_user.id), day_info=day_info)
    await state.clear()


@router.message(StateFilter(None), F.text.lower() == "отметить начало ночного сна 🌃")
async def start_night_sleep_time(message: Message, state: FSMContext):
    await state.set_state(Night.start_night_sleep_time)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отметить окончание ночного сна 🌅")]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    await message.answer(
        "Когда вы уснули ночью? (Введите время в формате ЧЧ:ММ)",
        reply_markup=keyboard,
    )
