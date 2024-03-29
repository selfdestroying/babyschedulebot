import asyncio

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)
from arq import ArqRedis

from src.bot.filters.register import RegisterFilter
from src.bot.handlers.menu import MenuGroup
from src.bot.handlers.register.fsm import RegisterGroup
from src.bot.keyboards.menu import MENU_KEYBOARD
from src.phrases import ru

start_router = Router(name="start")


@start_router.message(CommandStart(), RegisterFilter())
async def start_w_register(message: Message, state: FSMContext, arqredis: ArqRedis):
    await state.clear()
    id = message.from_user.id
    user_name = message.from_user.first_name
    await state.set_state(RegisterGroup.user_problem)
    await state.set_data({"id": id, "user_name": user_name})
    await message.answer(ru.HELLO.format(user_name))
    await asyncio.sleep(2)
    await message.answer(ru.ABOUT_1)
    await asyncio.sleep(2)
    await message.answer(ru.ASK_PROBLEM)


@start_router.message(Command("clear"))
async def clear(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Состояние очищено")


@start_router.message(Command("menu"))
async def menu(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    await state.set_state(MenuGroup.menu)
    await message.answer("Главное меню", reply_markup=MENU_KEYBOARD)


# @router.message(RegisterGroup.user_problem)
# async def test(message: Message, state: FSMContext):
#     await state.clear()
#     print(await state.get_state())
#     print(await state.get_data())
#     await message.answer("test")


# # TODO: refactor
# class Day(StatesGroup):
#     start = State()
#     end = State()


# @router.message(StateFilter(None), F.text == "Отметить начало ночного сна 🌃")
# async def start_night_sleep_time(message: Message, state: FSMContext):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="Да", callback_data="start_night_yes"),
#                 InlineKeyboardButton(text="Нет", callback_data="start_night_no"),
#             ],
#         ]
#     )
#     await message.answer(
#         "⚠️ Вы уверены, что хотите отметить начало ночного сна? Это приведет к завершению сегодняшнего дня и подведению статистики.",
#         reply_markup=keyboard,
#     )


# @router.callback_query(F.data == "start_night_yes")
# async def start_night_sleep_time_yes(callback_query: CallbackQuery, state: FSMContext):
#     await state.set_state(Night.start_night_sleep_time)
#     await callback_query.message.answer(
#         "Когда вы уснули ночью? (Введите время в формате ЧЧ:ММ)",
#         reply_markup=BACK_KEYBOARD,
#     )


# @router.callback_query(F.data == "start_night_no")
# async def start_night_sleep_time_no(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.message.delete()
#     await state.clear()


# @router.message(F.text == "Отметить время дневного сна ☀️")
# async def note_sleep_message(message: Message, state: FSMContext):
#     await state.set_state(Day.start)
#     await message.answer("Во сколько уснули?")


# @router.callback_query(F.data == "day_sleep")
# async def note_sleep_callback(callback_query: CallbackQuery, state: FSMContext):
#     await state.set_state(Day.start)
#     await callback_query.message.answer("Во сколько уснули?")
#     await callback_query.answer()


# @router.message(Command("stats"))
# async def text(message: Message, state: FSMContext):
#     id = message.from_user.id
#     current_date = datetime.now(pytz.timezone("Etc/GMT-3"))
#     current_date_str = current_date.strftime("%Y-%m-%d")
#     schedule = scheduleapi.read(user_id=id, date=current_date_str)
#     child = childapi.read(user_id=message.from_user.id)
#     child_name = child.get("name")
#     age = child.get("age")

#     end_night_time = schedule.get("start_day") or "-"
#     sleeps = schedule.get("sleeps") or []
#     start_night_time = schedule.get("start_prev_night") or "-"

#     html_child_info_text = f"👶 <b>{child_name}</b> - {age} месяцев\n\n"
#     sleeps_text = ""
#     for i in range(len(sleeps)):
#         sleeps_text += f"\n{i+1} сон: {sleeps[i]['start_sleep_time'][:5]} - {sleeps[i]['end_sleep_time'][:5]}"
#     html_schedule_text = f"<i>{current_date.strftime('%d.%m.%Y')}</i>\n<b>Уснули:</b> {start_night_time}\n<b>Проснулись:</b> {end_night_time}\n{sleeps_text}"

#     await message.answer(text=html_child_info_text + html_schedule_text)


# @router.callback_query(F.data == "night_sleep")
# async def night_sleep(callback_query: CallbackQuery, state: FSMContext):
#     await state.set_state(Night.start)
#     await callback_query.message.answer("Когда вы уснули ночью? 🌙")
#     await callback_query.answer()


# # @router.message(Night.start, TimeFilter())
# # async def start_night(message: Message, state: FSMContext):
# #     await state.update_data(start_night=message.text)
# #     await state.set_state(Night.end)
# #     await message.answer("Когда вы проснулись утром? ☀️")


# # @router.message(Night.end, TimeFilter())
# # async def end_night(message: Message, state: FSMContext):
# #     await state.update_data(end_night=message.text)

# #     child = childapi.read(user_id=message.from_user.id)
# #     child_name = child.get("name")
# #     age = child.get("age")
# #     current_date = datetime.now()
# #     data = await state.get_data()
# #     end_night_time = data.get("end_night")
# #     sleeps = []
# #     start_night_time = data.get("start_night")
# #     html_child_info_text = f"👶 <b>{child_name}</b> - {age} месяцев\n\n"
# #     scheduleapi.create(
# #         message.from_user.id,
# #         current_date.strftime("%Y-%m-%d"),
# #         start_night_sleep_time=start_night_time,
# #         end_night_sleep_time=end_night_time,
# #         night_duration=calculate_minutes_difference(
# #             start_night_time + ":00", end_night_time + ":00"
# #         ),
# #         night_rating=0,
# #     )
# #     sleeps_text = ""
# #     for i in range(len(sleeps)):
# #         sleeps_text += f"\n{i+1} сон: {sleeps[i]['start_sleep_time'][:5]} - {sleeps[i]['end_sleep_time'][:5]}"
# #     html_schedule_text = f"<i>{current_date.strftime('%d.%m.%Y')}</i>\n<b>Уснули:</b> {start_night_time}\n<b>Проснулись:</b> {end_night_time}\n{sleeps_text}"

# #     keyboard = InlineKeyboardBuilder()
# #     day_sleep_button = InlineKeyboardButton(
# #         text="Отметить время дневного сна ☀️", callback_data="day_sleep"
# #     )
# #     night_sleep_button = InlineKeyboardButton(
# #         text="Отметить время ночного сна 🌙", callback_data="night_sleep"
# #     )
# #     profile_button = InlineKeyboardButton(text="Профиль 👤", callback_data="profile")
# #     keyboard.row(day_sleep_button)
# #     keyboard.row(night_sleep_button)
# #     keyboard.row(profile_button)

# #     await message.answer(
# #         text=html_child_info_text + html_schedule_text,
# #         reply_markup=keyboard.as_markup(),
# #     )
# #     average_duration = ideal_data.ideal_data[age]["day"]["activity"][
# #         "average_duration"
# #     ]
# #     average_duration = sum(average_duration) / len(average_duration)

# #     result = (
# #         datetime.strptime(end_night_time, "%H:%M") + timedelta(minutes=average_duration)
# #     ).strftime("%H:%M")

# #     await message.answer(
# #         text=f"Вы проснулись в {end_night_time}. Следующий ваш сон должен начаться в {result}",
# #     )
# #     await send_message_with_delay(message, 5)
# #     await state.clear()


# @router.message(Day.start, TimeFilter())
# async def start_day(message: Message, state: FSMContext):
#     await state.update_data(start_day=message.text)
#     await state.set_state(Day.end)
#     await message.answer("Во сколько проснулись?")


# @router.message(Day.end, TimeFilter())
# async def end_day(message: Message, state: FSMContext):
#     await state.update_data(end_day=message.text)
#     data = await state.get_data()
#     start_sleep = data.get("start_day")
#     end_sleep = data.get("end_day")
#     current_date = datetime.now(pytz.timezone("Etc/GMT-3")).strftime("%Y-%m-%d")

#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="Отметить дневной сон", callback_data="day_sleep"
#                 )
#             ]
#         ]
#     )

#     start_sleep = datetime.strptime(
#         current_date + " " + start_sleep, "%Y-%m-%d %H:%M"
#     ).replace(tzinfo=pytz.timezone("Etc/GMT-3"))
#     end_sleep = datetime.strptime(
#         current_date + " " + end_sleep, "%Y-%m-%d %H:%M"
#     ).replace(tzinfo=pytz.timezone("Etc/GMT-3"))
#     age = childapi.read(user_id=message.from_user.id)["age"]
#     sleep = [
#         {
#             "start_sleep_time": start_sleep.strftime("%H:%M"),
#             "end_sleep_time": end_sleep.strftime("%H:%M"),
#             "sleep_duration": calculate_minutes_difference(
#                 start_sleep.strftime("%H:%M:%S"), end_sleep.strftime("%H:%M:%S")
#             ),
#         }
#     ]
#     recommendation = compare_day_sleep(
#         sleep, age=age, idealdata=ideal_data.ideal_data
#     )
#     current_time = datetime.now(pytz.timezone("Etc/GMT-3"))
#     ideal_time = ideal_data.ideal_data[age]["day"]["activity"]["average_duration"]

#     ideal_time_left = ideal_time[0]
#     ideal_time_right = ideal_time[1]

#     next_sleep_start_left = end_sleep + timedelta(minutes=ideal_time_left)
#     next_sleep_start_right = end_sleep + timedelta(minutes=ideal_time_right)
#     next_sleep_delta = next_sleep_start_right - current_time
#     print(next_sleep_delta.seconds)
#     print(ideal_time_right)
#     print(current_time.minute)
#     note_sleep_button = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="Записать еще один сон", callback_data="day_sleep"
#                 )
#             ]
#         ]
#     )
#     if current_time < end_sleep:
#         await message.answer("Вы указали будущее время, так нельзя))))")
#     else:
#         scheduleapi.update_sleeps(
#             user_id=message.from_user.id,
#             date=current_date,
#             sleep={
#                 "start_sleep_time": start_sleep + ":00",
#                 "end_sleep_time": end_sleep + ":00",
#                 "sleep_duration": calculate_minutes_difference(
#                     start_sleep + ":00", end_sleep + ":00"
#                 ),
#             },
#         )
#         await state.clear()
#         if current_time > next_sleep_start_right:
#             await message.answer(
#                 f"Сон записан. {recommendation}", reply_markup=note_sleep_button
#             )
#         else:
#             await message.answer(
#                 f"Вы проснулись в {end_sleep.strftime('%H:%M')}. {recommendation}Следующий ваш сон должен начаться примерно в {next_sleep_start_left.strftime('%H:%M')} - {next_sleep_start_right.strftime('%H:%M')}\n<i>Я пришлю вам напоминание, когда придет время засыпать</i>",
#                 reply_markup=ReplyKeyboardRemove(),
#             )
#             await send_message_with_delay(message, next_sleep_delta.seconds)


# async def send_message_with_delay(message: Message, delay: int):
#     await asyncio.sleep(delay)
#     await message.answer(text="Уснули?", reply_markup=MENU_KEYBOARD)
