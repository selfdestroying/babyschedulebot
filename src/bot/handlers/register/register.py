from datetime import datetime

from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram_calendar import DialogCalendar, DialogCalendarCallback

from src.bot.handlers.register import router
from src.bot.handlers.register.fsm import RegisterGroup
from src.bot.handlers.register.helpers import register_user_and_child
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.bot.keyboards.register import (
    CHILD_GENDER_KEYBOARD,
    SEND_PHONE_KEYBOARD,
    get_calendar_keyboard,
)
from src.config import conf
from src.locales.ru import TEXT


@router.message(F.text == "Начать регистрацию", RegisterGroup.confirmation)
async def register_confirmation(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(user_name=message.from_user.full_name)
    await state.set_state(RegisterGroup.user_phone)
    await message.answer(TEXT["ru"]["ask_user_phone"], reply_markup=SEND_PHONE_KEYBOARD)


@router.message(
    RegisterGroup.user_phone,
    F.contact,
)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.contact.phone_number)
    await state.set_state(RegisterGroup.user_email)
    await message.answer(TEXT["ru"]["ask_user_email"])


@router.message(
    RegisterGroup.user_email,
    F.text.regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
)
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    await state.set_state(RegisterGroup.user_problem)
    await message.answer(TEXT["ru"]["ask_problem"])


@router.message(RegisterGroup.user_problem)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(RegisterGroup.child_name)
    await message.answer(TEXT["ru"]["ask_child_name"])


@router.message(RegisterGroup.child_name)
async def child_name(message: Message, state: FSMContext):
    await state.update_data(child_name=message.text)
    await state.set_state(RegisterGroup.child_birth_date)
    await message.answer(
        TEXT["ru"]["ask_child_age"],
        reply_markup=await get_calendar_keyboard(),
    )


@router.callback_query(DialogCalendarCallback.filter())
async def process_child_birth_date(
    callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    selected, date = await DialogCalendar(locale=conf.locale).process_selection(
        callback_query, callback_data
    )
    print(date)
    if selected:
        if date > datetime.now():
            await callback_query.message.edit_text(
                "Нельзя выбрать будущую дату ❌. Выберите другую дату.",
                reply_markup=await get_calendar_keyboard(),
            )
        else:
            await state.update_data(child_birth_date=date)
            await state.set_state(RegisterGroup.child_gender)
            await callback_query.message.edit_text(
                "Выбранная дата: {}".format(date.strftime("%d.%m.%Y"))
            )
            await callback_query.message.answer(
                TEXT["ru"]["ask_child_gender"], reply_markup=CHILD_GENDER_KEYBOARD
            )


@router.callback_query(RegisterGroup.child_gender, F.data.in_(["male", "female"]))
async def child_gender(call: CallbackQuery, state: FSMContext):
    await state.update_data(child_gender=call.data)
    await state.set_state(RegisterGroup.food_type)
    await call.message.edit_text(TEXT["ru"]["ask_food_type"])
    await call.answer()


@router.message(RegisterGroup.food_type)
async def food_type(message: Message, state: FSMContext):
    await state.update_data(food_type=message.text)
    data = await state.get_data()
    register_user_and_child(data)
    await state.clear()
    await message.answer("Регистрация прошла успешно!", reply_markup=MENU_KEYBOARD)


# -------------------------------------------------------------

# @router.message(RegisterGroup.child_birth_date)
# async def wrong_child_birth_date(message: Message):
#     await message.answer(
#         "Выберите дату с помощью клавиатуры",
#         reply_markup=get_calendar_keyboard(),
#     )

# @router.message(RegisterGroup.user_phone)
# async def wrong_user_phone(message: Message):
#     await message.answer("Пожалуйста, поделитесь своим номером с помощью кнопки ниже ⬇️")


# @router.message(RegisterGroup.user_email)
# async def wrong_user_email(message: Message):
#     await message.answer("Пожалуйста, введите корректный адрес электронной почты")
