from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from db.user import save_user_data
from keyboards.child_gender import get_child_gender_kb
from keyboards.menu import get_main_menu_kb
from locales.ru import TEXT
from models.Child import Child
from models.User import User

router = Router()


# TODO: replace all code below with aiogram-dialog
class UserData(StatesGroup):
    user_problem = State()
    child_gender = State()
    child_name = State()
    child_age = State()
    food_type = State()
    user_phone = State()
    user_email = State()


@router.message(UserData.user_problem)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(UserData.child_gender)
    await message.answer(TEXT["ru"]["understand"])
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
    await state.set_state(UserData.child_age)
    await message.answer(TEXT["ru"]["ask_child_age"])


# TODO: Add age validation
@router.message(UserData.child_age)
async def child_age(message: Message, state: FSMContext):
    await state.update_data(child_age=message.text)
    await state.set_state(UserData.food_type)
    await message.answer(TEXT["ru"]["ask_food_type"])


@router.message(UserData.food_type)
async def foodtype(message: Message, state: FSMContext):
    await state.update_data(food_type=message.text)
    await state.set_state(UserData.user_phone)
    await message.answer(TEXT["ru"]["ask_user_phone"])


# TODO: Add phone number validation
@router.message(UserData.user_phone)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.text)
    await state.set_state(UserData.user_email)
    await message.answer(TEXT["ru"]["ask_user_email"])


# TODO: Add email validation
@router.message(UserData.user_email)
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    data = await state.get_data()
    child = Child(
        name=data["child_name"],
        gender=data["child_gender"],
        age=data["child_age"],
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
