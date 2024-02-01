from datetime import datetime

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram_calendar import DialogCalendar, DialogCalendarCallback, get_user_locale
from db.user import save_user_data
from keyboards.child_gender import get_child_gender_kb
from keyboards.menu import get_main_menu_kb
from locales.ru import TEXT
from models.Child import Child
from models.User import User
from utils.differences import calculate_child_age_in_months

router = Router()


class UserData(StatesGroup):
    user_problem = State()
    child_gender = State()
    child_name = State()
    child_birth_date = State()
    food_type = State()
    user_phone = State()
    user_email = State()


@router.message(UserData.user_problem)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(UserData.child_gender)
    await message.answer(
        TEXT["ru"]["ask_child_gender"],
        reply_markup=get_child_gender_kb(),
    )


@router.callback_query(UserData.child_gender, F.data.in_(["male", "female"]))
async def child_gender(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        child_gender="Мальчик" if call.data == "male" else "Девочка"
    )
    await state.set_state(UserData.child_name)
    await call.message.edit_text(TEXT["ru"]["ask_child_name"])
    await call.answer()


@router.message(UserData.child_name)
async def child_name(message: Message, state: FSMContext):
    await state.update_data(child_name=message.text)
    await state.set_state(UserData.child_birth_date)
    await message.answer(
        TEXT["ru"]["ask_child_age"],
        reply_markup=await DialogCalendar(
            locale=await get_user_locale(message.from_user),
        ).start_calendar(),
    )


@router.callback_query(DialogCalendarCallback.filter())
async def process_child_birth_date(
    callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    selected, date = await DialogCalendar(
        locale=await get_user_locale(callback_query.from_user)
    ).process_selection(callback_query, callback_data)
    print(selected)
    if selected:
        if date > datetime.now():
            await callback_query.message.edit_text(
                "Нельзя выбрать будущую дату ❌. Выберите другую дату.",
                reply_markup=await DialogCalendar(
                    locale=await get_user_locale(callback_query.from_user),
                ).start_calendar(),
            )
        else:
            await state.update_data(child_birth_date=date)
            await callback_query.message.edit_text(
                "Выбранная дата: {}".format(date.strftime("%d.%m.%Y"))
            )
            await callback_query.message.answer(TEXT["ru"]["ask_food_type"])
            await state.set_state(UserData.food_type)


@router.message(UserData.food_type)
async def food_type(message: Message, state: FSMContext):
    await state.update_data(food_type=message.text)
    await state.set_state(UserData.user_phone)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]
        ],
        resize_keyboard=True,
    )
    await message.answer(TEXT["ru"]["ask_user_phone"], reply_markup=keyboard)


@router.message(
    UserData.user_phone,
    F.contact,
)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.contact.phone_number)
    await state.set_state(UserData.user_email)
    await message.answer(
        TEXT["ru"]["ask_user_email"], reply_markup=ReplyKeyboardRemove()
    )


@router.message(
    UserData.user_email,
    F.text.regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
)
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    data = await state.get_data()
    age = calculate_child_age_in_months(data["child_birth_date"])
    child = Child(
        name=data["child_name"],
        gender=data["child_gender"],
        birth_date=data["child_birth_date"].strftime("%d.%m.%Y"),
        age=age,
        food_type=data["food_type"],
    )
    user = User(
        name=message.from_user.first_name,
        phone=data["user_phone"],
        email=data["user_email"],
        child=child,
        schedule={},
    )
    save_user_data(message.from_user.id, user)
    await message.answer(TEXT["ru"]["done"], reply_markup=get_main_menu_kb())
    await state.clear()


@router.message(UserData.child_birth_date)
async def wrong_child_birth_date(message: Message):
    await message.answer(
        "Выберите дату с помощью клавиатуры",
        reply_markup=await DialogCalendar(
            locale=await get_user_locale(message.from_user),
        ).start_calendar(),
    )


@router.message(UserData.user_phone)
async def wrong_user_phone(message: Message):
    await message.answer("Пожалуйста, поделитесь своим номером с помощью кнопки ниже ⬇️")


@router.message(UserData.user_email)
async def wrong_user_email(message: Message):
    await message.answer("Пожалуйста, введите корректный адрес электронной почты")
