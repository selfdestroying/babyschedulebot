import asyncio
from datetime import datetime

import pytz
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardRemove,
)
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from arq import ArqRedis
from arq.jobs import Job

from src.api.analysis import ideal_data
from src.bot.filters.register import EmailFilter
from src.bot.filters.time import TimeFilter
from src.bot.handlers.menu import MenuGroup
from src.bot.handlers.register.fsm import RegisterGroup
from src.bot.handlers.register.helpers import (
    register_child,
    register_schedule,
    register_user,
)
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.bot.keyboards.night import get_rate_kb
from src.bot.keyboards.register import (
    FOOD_TYPE_KEYBOARD,
    GENDER_KEYBOARD,
    REGISTER_CONFIRM_KEYBOARD,
    SEND_PHONE_KEYBOARD,
    get_calendar_keyboard,
)
from src.config import conf
from src.phrases import ru
from src.utils.differences import (
    calculate_age_in_months,
)
from src.utils.remind import calculate_time_to_remind

register_router = Router(name="register")


@register_router.message(RegisterGroup.user_problem, F.text)
async def user_problem(message: Message, state: FSMContext) -> None:
    await state.update_data(user_problem=message.text)
    await state.set_state(RegisterGroup.confirmation)
    await message.answer(ru.ABOUT_2)
    await asyncio.sleep(2)
    await message.answer(ru.REGISTER_CONFIRM, reply_markup=REGISTER_CONFIRM_KEYBOARD)


@register_router.message(RegisterGroup.confirmation, F.text == "Начать регистрацию")
async def register_confirmation(message: Message, state: FSMContext):
    await state.set_state(RegisterGroup.user_phone)
    await message.answer(ru.ASK_PHONE, reply_markup=SEND_PHONE_KEYBOARD)


@register_router.message(RegisterGroup.confirmation)
async def register_confirmation_wrong(message: Message, state: FSMContext):
    await message.answer(ru.REGISTER_CONFIRM, reply_markup=REGISTER_CONFIRM_KEYBOARD)


@register_router.message(
    RegisterGroup.user_phone, (F.contact) & (F.from_user.id == F.contact.user_id)
)
async def user_phone(message: Message, state: FSMContext):
    await state.update_data(user_phone=message.contact.phone_number)
    await state.set_state(RegisterGroup.user_email)
    await message.answer(ru.ASK_EMAIL, reply_markup=ReplyKeyboardRemove())


@register_router.message(RegisterGroup.user_phone)
async def user_phone_wrong(message: Message, state: FSMContext):
    await message.answer(ru.ASK_PHONE, reply_markup=SEND_PHONE_KEYBOARD)


@register_router.message(RegisterGroup.user_email, EmailFilter())
async def user_email(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    await state.set_state(RegisterGroup.gender)
    await message.answer(ru.ABOUT_3)
    await asyncio.sleep(2)
    await message.answer(ru.ASK_GENDER, reply_markup=GENDER_KEYBOARD)


@register_router.message(RegisterGroup.user_email)
async def user_email_wrong(message: Message, state: FSMContext):
    await message.answer(ru.ASK_EMAIL)


@register_router.callback_query(RegisterGroup.gender, F.data.in_(["male", "female"]))
async def gender(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback_query.data)
    await state.set_state(RegisterGroup.child_name)
    await callback_query.message.edit_text(
        "Девочка" if gender == "female" else "Мальчик"
    )
    await callback_query.message.answer(ru.ASK_CHILD_NAME)
    await callback_query.answer()


@register_router.message(RegisterGroup.child_name, F.text)
async def child_name(message: Message, state: FSMContext):
    data = await state.get_data()
    gender = data["gender"]
    child_name = message.text
    await state.update_data(child_name=child_name)
    await state.set_state(RegisterGroup.child_birth_date)
    await message.answer(
        ru.ASK_CHILD_BIRTH_DATE[gender].format(child_name),
        reply_markup=await get_calendar_keyboard(),
    )


@register_router.callback_query(DialogCalendarCallback.filter())
async def process_child_birth_date(
    callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    selected, date = await DialogCalendar(locale=conf.locale).process_selection(
        callback_query, callback_data
    )
    if selected:
        if date > datetime.now():
            await callback_query.message.edit_text(
                "Нельзя выбрать будущую дату ❌. Выберите другую дату.",
                reply_markup=await get_calendar_keyboard(),
            )
        else:
            date = date.strftime("%Y-%m-%d")
            age = calculate_age_in_months(date)
            ideal_data_for_age = ideal_data.ideal_data[age]
            await state.update_data(child_birth_date=date)
            await state.update_data(age=age)
            await state.update_data(ideal_data_for_age=ideal_data_for_age)
            await state.set_state(RegisterGroup.food_type)
            await callback_query.message.edit_text(date)
            await callback_query.message.answer(
                ru.ASK_FOOD_TYPE, reply_markup=FOOD_TYPE_KEYBOARD
            )


@register_router.callback_query(
    RegisterGroup.food_type, F.data.in_(["breast", "formula", "mix"])
)
async def food_type(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(food_type=callback_query.data)
    data = await state.get_data()
    register_user(data=data)
    register_child(data=data)
    await state.set_state(RegisterGroup.start_night_time)
    await callback_query.message.edit_text(
        "Грудь"
        if data["food_type"] == "breast"
        else "Смесь"
        if data["food_type"] == "formula"
        else "Грудь и смесь"
    )
    await callback_query.message.answer(ru.ABOUT_4)
    await asyncio.sleep(2)
    await callback_query.message.answer(ru.ABOUT_5)
    await asyncio.sleep(2)
    await callback_query.message.answer(ru.ABOUT_6)
    await asyncio.sleep(2)
    await callback_query.message.answer(ru.ASK_PREV_NIGHT)
    await asyncio.sleep(2)
    await callback_query.message.answer(
        ru.ASK_PREV_NIGHT_START_SLEEP[data.get("gender")].format(data.get("child_name"))
    )
    await callback_query.answer()


# @register_router.message(StateFilter(RegisterGroup), F.text == "Исправить 🔙")
# async def correct_answer(message: Message, state: FSMContext):
#     current_state = await state.get_state()

#     print(current_state)
#     if current_state == "RegisterGroup:gender":
#         await state.set_state(RegisterGroup.child_name)
#         await message.answer(ru.ASK_CHILD_NAME)
#     elif current_state == "RegisterGroup:child_birth_date":
#         await state.set_state(RegisterGroup.gender)
#         await message.answer(ru.ASK_gender, reply_markup=gender_KEYBOARD)
#     elif current_state == "RegisterGroup:food_type":
#         data = await state.get_data()
#         child_name = data["child_name"]
#         gender = data["gender"]
#         await state.set_state(RegisterGroup.child_birth_date)
#         await message.answer(
#             ru.ASK_CHILD_BIRTH_DATE[gender].format(child_name),
#             reply_markup=await get_calendar_keyboard(),
#         )
#     elif current_state == "RegisterGroup:end_night_time":
#         await state.set_state(RegisterGroup.food_type)
#         await message.answer(ru.ASK_FOOD_TYPE, reply_markup=FOOD_TYPE_KEYBOARD)


@register_router.message(RegisterGroup.start_night_time, TimeFilter())
async def start_night_time(message: Message, state: FSMContext):
    data = await state.get_data()
    gender = data["gender"]
    child_name = data["child_name"]
    await state.update_data(start_night_time=message.text + ":00")
    await state.set_state(RegisterGroup.end_night_time)
    await message.answer(
        ru.ASK_PREV_NIGHT_END_SLEEP[gender].format(child_name),
        reply_markup=ReplyKeyboardRemove(),
    )


@register_router.message(RegisterGroup.end_night_time, TimeFilter())
async def end_night_time(message: Message, state: FSMContext):
    data = await state.get_data()
    child_name = data["child_name"]
    gender = data["gender"]
    await state.update_data(end_night_time=message.text + ":00")
    await state.set_state(RegisterGroup.night_wake_up_count)
    await message.answer(ru.ASK_NIGHT_WAKE_UP_COUNT[gender].format(child_name))


@register_router.message(RegisterGroup.start_night_time)
@register_router.message(RegisterGroup.end_night_time)
async def night_time_wrong(message: Message, state: FSMContext):
    await message.answer(ru.WRONG_TIME)


@register_router.message(RegisterGroup.night_wake_up_count, F.text.regexp(r"^(\d+)$"))
async def night_wake_up_count(message: Message, state: FSMContext):
    await state.update_data(night_wake_up_count=int(message.text))
    await state.set_state(RegisterGroup.night_rating)
    await message.answer(ru.ASK_NIGHT_RATING, reply_markup=get_rate_kb())


@register_router.message(RegisterGroup.night_wake_up_count)
async def night_wake_up_count_wrong(message: Message, state: FSMContext):
    data = await state.get_data()
    child_name = data["child_name"]
    gender = data["gender"]
    await message.answer(ru.ASK_NIGHT_WAKE_UP_COUNT[gender].format(child_name))


@register_router.callback_query(
    RegisterGroup.night_rating,
    F.data.in_(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
)
async def night_rating(
    callback_query: CallbackQuery, state: FSMContext, arqredis: ArqRedis
):
    night_rating = int(callback_query.data)
    await state.update_data(night_rating=night_rating)
    await callback_query.message.edit_text(f"{callback_query.data} ⭐")
    if 1 <= night_rating <= 4:
        await callback_query.message.answer(ru.NIGHT_RATING_1_4)
    elif 5 <= night_rating <= 7:
        await callback_query.message.answer(ru.NIGHT_RATING_5_7)
    elif 8 <= night_rating <= 10:
        await callback_query.message.answer(ru.NIGHT_RATING_8_10)

    data = await state.get_data()
    child_name = data.get("child_name")
    gender = data.get("gender")
    age = data.get("age")
    wake_up_time = data.get("end_night_time")
    message_send_time = datetime.now(pytz.timezone("Etc/GMT-3")).strftime("%H:%M:%S")
    average_activity_duration = ideal_data.ideal_data[age]["day"]["activity"][
        "average_duration"
    ]
    time_to_remind = calculate_time_to_remind(
        wake_up_time, message_send_time, average_activity_duration
    )
    if time_to_remind:
        await callback_query.message.answer(
            ru.GOOD_MORNING[gender].format(
                child_name,
                wake_up_time[:5],
                time_to_remind["activity_duration_min"],
                time_to_remind["activity_duration_max"],
                time_to_remind["next_fall_asleep_time_min"],
                time_to_remind["next_fall_asleep_time_max"],
            )
        )
        day_fall_asleep_job_id: Job = await arqredis.enqueue_job(
            "send_message",
            _defer_by=time_to_remind["time_to_remind"],
            chat_id=callback_query.from_user.id,
            text="Уснули?",
        )
        await state.update_data(day_fall_asleep_job_id=day_fall_asleep_job_id.job_id)
    await callback_query.message.answer(
        ru.PRESS_END_DAY_SLEEP_BUTTON, reply_markup=MENU_KEYBOARD
    )
    register_schedule(data=data)
    await state.set_state(MenuGroup.menu)
    await callback_query.answer()


# @router.message(RegisterGroup.end_night_time, TimeFilter())
# async def end_night_time(message: Message, state: FSMContext):
#     await state.update_data(end_night_time=message.text)
#     data = await state.get_data()
#     end_night_time = data.get("end_night_time")
#     start_prev_night = data.get("start_night_time")
#     current_date = datetime.now(pytz.timezone("Etc/GMT-3")).strftime("%Y-%m-%d")
#     end_night_time = datetime.strptime(
#         f"{current_date} {end_night_time}", "%Y-%m-%d %H:%M"
#     ).replace(tzinfo=pytz.timezone("Etc/GMT-3"))
#     current_time = datetime.now(pytz.timezone("Etc/GMT-3"))
#     age = childapi.read(user_id=message.from_user.id)["age"]

#     ideal_time = ideal_data.ideal_data[age]["day"]["activity"]["average_duration"]

#     ideal_time_left = ideal_time[0]
#     ideal_time_right = ideal_time[1]

#     next_sleep_start_left = end_night_time + timedelta(minutes=ideal_time_left)
#     next_sleep_start_right = end_night_time + timedelta(minutes=ideal_time_right)
#     next_sleep_delta = next_sleep_start_right - current_time
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="Записать еще один сон", callback_data="day_sleep"
#                 )
#             ]
#         ]
#     )

#     if current_time < end_night_time:
#         await message.answer("Вы указали будущее время, так нельзя))))")
#     else:
#         scheduleapi.create(
#             user_id=message.from_user.id,
#             date=current_date,
#             start_day=end_night_time.strftime("%H:%M:%S"),
#             start_prev_night=start_prev_night + ":00",
#             night_duration=calculate_minutes_difference(
#                 start_prev_night + ":00", end_night_time.strftime("%H:%M:%S")
#             ),
#             night_rating=10,
#         )
#         await state.clear()
#         await message.answer(
#             "Информация по прошлой ночи записана. Теперь можем начинать вести статистику по сегоднящнему дню.\n\n<i>Так же вы в любой момент можете посмотреть статистику за сегоднящний день с помощью команды /stats или вызвать клавиатуру с помощью команды /menu</i>"
#         )
#         if current_time > next_sleep_start_right:
#             await message.answer(
#                 f"Вы проснулись в {end_night_time.strftime('%H:%M')} утра. Для точности статистики, отметьте, пожалуйста <b>прошедшие</b> дневные сны",
#                 reply_markup=keyboard,
#             )
#         else:
#             await message.answer(
#                 f"Вы проснулись в {end_night_time.strftime('%H:%M')} утра. Следующий ваш сон должен начаться примерно в {next_sleep_start_left.strftime('%H:%M')} - {next_sleep_start_right.strftime('%H:%M')}\n<i>Я пришлю вам напоминание, когда придет время засыпать</i>",
#                 reply_markup=ReplyKeyboardRemove(),
#             )
#             await asyncio.sleep(next_sleep_delta.seconds)
#             await message.answer("Уснули?", reply_markup=MENU_KEYBOARD)


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
