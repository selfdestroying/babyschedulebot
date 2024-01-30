from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.markdown import hbold
from db.user import get_user_by_id, save_user_data
from handlers.registration import UserData
from keyboards.menu import get_main_menu_kb
from locales.ru import TEXT
from models.User import User
from test_data import test_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    id = str(message.from_user.id)
    user = get_user_by_id(id)
    if user:
        await message.answer(
            "Вы в главном меню. Выберите нужную команду при помощи кнопки",
            reply_markup=get_main_menu_kb(),
        )
    else:
        await message.answer(
            TEXT["ru"]["start"].format(hbold(message.from_user.first_name))
        )
        # @DEV
        await message.answer(
            "For development purposes only",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Generate test data", callback_data="test_data"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Continue without test data",
                            callback_data="no_test_data",
                        )
                    ],
                ]
            ),
        )
        # await message.answer(TEXT["ru"]["ask_problem"])
        # await state.set_state(UserData.user_problem)


# @DEV
@router.callback_query(F.data == "test_data")
async def test_data(call: CallbackQuery):
    user = User(**test_user)
    save_user_data(call.from_user.id, user)
    await call.message.delete()
    await call.message.answer(
        "Вы в главном меню. Выберите нужную команду при помощи кнопки",
        reply_markup=get_main_menu_kb(),
    )


# @DEV
@router.callback_query(F.data == "no_test_data")
async def no_test_data(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(TEXT["ru"]["ask_problem"])
    await call.state.set_state(UserData.user_problem)
