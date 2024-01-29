from aiogram import F, Router
from aiogram.types import Message
from db.user import get_user_by_id

router = Router()


@router.message(F.text == "Информация ℹ️")
async def info(message: Message):
    user = get_user_by_id(str(message.from_user.id))
    name = user.name
    phone = user.phone
    email = user.email
    child_name = user.child.name
    child_age = user.child.age
    child_gender = user.child.gender
    food_type = user.child.food_type

    html_info_text = "Информация о <b>родителе 🧑</b>\nИмя: {}\nТелефон: {}\nEmail: {}\nИнформация о <b>ребенке 👶</b>\nИмя: {}\nВозраст: {}\nПол: {}\nТип питания: {}".format(
        name, phone, email, child_name, child_age, child_gender, food_type
    )

    await message.answer(html_info_text)
