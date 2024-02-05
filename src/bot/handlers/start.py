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

from src.api.dbapi import childapi, userapi
from src.bot.filters.register import RegisterFilter
from src.bot.handlers.register.register import RegisterGroup
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.bot.keyboards.register import REGISTER_START_CONFIRM
from src.locales.ru import TEXT
from src.utils.test_data import test_child, test_user

router = Router()


@router.message(CommandStart(), RegisterFilter())
async def start_w_register(message: Message):
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


@router.message(CommandStart())
async def start_wo_register(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Вы в главном меню. Выберите нужную команду при помощи кнопки",
        reply_markup=MENU_KEYBOARD,
    )


# @DEV
@router.callback_query(F.data == "test_data")
async def test_data(call: CallbackQuery):
    id = call.from_user.id
    userapi.create(id, **test_user)
    childapi.create(user_id=id, **test_child)
    await call.message.delete()
    await call.message.answer(
        "Вы в главном меню. Выберите нужную команду при помощи кнопки",
        reply_markup=MENU_KEYBOARD,
    )


# @DEV
@router.callback_query(F.data == "no_test_data")
async def no_test_data(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(RegisterGroup.confirmation)
    await call.message.answer(
        "Для того, чтобы начать регистрацию, нажми на кнопку внизу!",
        reply_markup=REGISTER_START_CONFIRM,
    )
