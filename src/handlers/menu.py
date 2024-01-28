from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold


from db.user import get_user_by_id
from handlers.registration import UserData
from keyboards.menu import get_main_menu_kb
from locales.ru import TEXT


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
        await message.answer(TEXT["ru"]["ask_problem"])
        await state.set_state(UserData.user_problem)
