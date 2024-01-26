import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler,
)

import numpy as np
import time
import json
from datetime import datetime


# Define states for the conversation
(
    GET_USER_NAME,
    GET_USER_PROBLEM,
    GET_CHILD_GENDER,
    GET_CHILD_NAME,
    GET_CHILD_AGE,
    GET_FOODTYPE,
    GET_USER_PHONE,
    GET_USER_EMAIL,
    GET_SCHEDULE,
    GET_FALL_ASLEEP_TIME,
    GET_WAKE_UP_TIME,
    GET_START_NIGHT_SLEEP,
    GET_DAY_RATING,
    SHOW_DAY_STATS,
    GET_END_NIGHT_SLEEP,
    GET_NIGHT_RATING,
    SHOW_NIGHT_STATS,
) = range(17)


def add_to_json(schedule_data):
    with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
        data = json.load(json_file)
    data.update(schedule_data)
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# для расчёта в минутах времени между "аа:аа" и "бб:бб"
def calculate_time_difference(start_time, end_time):
    # Define the time format for parsing
    time_format = "%H:%M"

    # Convert the time strings to datetime objects
    start_time = datetime.strptime(start_time, time_format)
    end_time = datetime.strptime(end_time, time_format)

    # Calculate the time difference
    time_difference = end_time - start_time

    # Extract the total seconds and convert to hours and minutes
    total_seconds = time_difference.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    total_minutes = int(time_difference.total_seconds() / 60)

    # Return the time difference as a tuple (hours, minutes)
    return total_minutes


day_sleeps_durations = []


# возвращает количество минут сна, после получения времени начала и конца
def save_sleep_duration(data, i):
    sleep_durations = []
    schedule = data["schedule"]
    current_date = datetime.now().strftime("%d.%m")

    for k, v in schedule.items():
        if k.startswith(f"{current_date}_{i}"):
            sleep_durations.append(v)
    sleep_duration = calculate_time_difference(sleep_durations[0], sleep_durations[1])
    day_sleeps_durations.append(sleep_duration)
    data["schedule"][f"{current_date}_{i}_sleep_duration"] = sleep_duration


# добавляет в файл количество всех снов
def save_total_day_sleep_time(data):
    current_date = datetime.now().strftime("%d.%m")
    data["schedule"][f"{current_date}_total_day_sleep_duration"] = sum(
        day_sleeps_durations
    )
    day_sleeps_durations.clear()


async def start_command(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    context.user_data["personal_info"] = {
        "user_id": user_id,
        "user_name": user_name,
    }
    context.user_data["schedule"] = {}

    try:
        with open("newjsonfrombot.json", "r") as file:
            user_id_in_file = json.load(file)
        if user_id == user_id_in_file["personal_info"]["user_id"]:
            # if user is in the base, starts asking schedule info
            print("user is in the base")
            return GET_SCHEDULE
    except:
        # asks for personal info if user is not in the base
        await update.message.reply_text(
            f"Привет {user_name}, я - искусственный интеллект, который помогает родителям легче взаимодействовать с детьми и радоваться жизни с малышом."
        )
        time.sleep(1)
        # @SELFDESTROYING НА ЧТО ВЛИЯЕТ ОТВЕТ?
        await update.message.reply_text("Расскажите, чем я могу вам помочь?")
        return GET_USER_PROBLEM


reply_keyboard = [["Мальчик", "Девочка"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def get_user_problem(update: Update, context: CallbackContext) -> int:
    context.user_data["personal_info"]["user_problem"] = update.message.text
    await update.message.reply_text(
        "Поняла. Будем с этим работать. \nМногие трудности, с которыми родители связаны с нарушением режима сна и бодрствования у малыша. Я помогу вам скорректировать режим так, чтобы ваш малыш рос довольным и развивался, а вы наслаждались родительством."
    )
    time.sleep(3)
    await update.message.reply_text("У вас мальчик или девочка?", reply_markup=markup)

    return GET_CHILD_GENDER


async def get_child_gender(update: Update, context: CallbackContext) -> int:
    context.user_data["personal_info"]["child_gender"] = update.message.text
    await update.message.reply_text("Как зовут вашего малыша?")

    return GET_CHILD_NAME


async def get_child_name(update: Update, context: CallbackContext) -> int:
    context.user_data["personal_info"]["child_name"] = update.message.text
    await update.message.reply_text(
        f"{context.user_data['personal_info']['child_name']} - прекрасное имя :)"
    )
    time.sleep(1)
    await update.message.reply_text("А сколько ему месяцев?")

    return GET_CHILD_AGE


async def get_child_age(update: Update, context: CallbackContext) -> int:
    context.user_data["personal_info"]["child_age"] = update.message.text
    await update.message.reply_text("Как вы кормите ребенка? ")

    return GET_FOODTYPE


async def get_foodtype(update: Update, context: CallbackContext) -> int:
    context.user_data["personal_info"]["foodtype"] = update.message.text
    await update.message.reply_text("Подскажите ваш номер телефона?")

    return GET_USER_PHONE


async def get_user_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["personal_info"]["user_phone"] = update.message.text
    await update.message.reply_text(
        "И напишите ваш email. На него я смогу прислать вам ваш дневник сна."
    )

    return GET_USER_EMAIL


async def get_user_email(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    context.user_data["personal_info"]["user_email"] = update.message.text

    # Send a message to the user without waiting for a reply
    await update.message.reply_text(
        "Отлично, вы зарегистрировались! Теперь давайте следить за графиком вашего малыша :)",
    )
    time.sleep(1)
    await context.bot.send_message(user_id, "Выберете в меню, что сейчас с малышом.")
    # Store user email and any other information if needed
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(context.user_data, json_file, ensure_ascii=False, indent=4)

    # Explicitly trigger the next state
    return GET_SCHEDULE


async def get_schedule(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    # Send a message to the user without waiting for a reply
    await context.bot.send_message(user_id, "Выберете в меню, что сейчас с малышом.")
    # @SELFDESTROYING В ЭТОЙ ФУНКЦИИ МЫ ТОЛЬКО ПРОСИМ ВЫБРАТЬ КОМАНДУ. САМА КОМАНДА ПРИЛЕТИТ В НЕКСТ СООБЩЕНИИ, КОТОРОЕ КАК РАЗ НУЖНО ЛОВИТЬ
    command = update.message.text.split()[0].lower()
    print(command)
    # Handle the command messages
    if command == "/daysleep":
        return GET_FALL_ASLEEP_TIME
    elif command == "/startnightsleep":
        return GET_START_NIGHT_SLEEP
    elif command == "/endnightsleep":
        return GET_END_NIGHT_SLEEP


async def get_start_night_sleep_time(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    # Ask about waking up time for the current activity
    await update.message.reply_text(f"Во сколько вы уснули в ночной сон?")

    current_date = datetime.now().strftime("%d.%m")

    # Save the user's reply as the waking up time for the current activity
    context.user_data["schedule"][
        f"{current_date}_start_night_sleep"
    ] = update.message.text
    add_to_json(context.user_data)

    # Move to the state for saving waking up time
    return GET_DAY_RATING


async def get_day_rating(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    # Ask about waking up time for the current activity
    await update.message.reply_text(f"Оцените сегодняшний день от 1 до 10")

    current_date = datetime.now().strftime("%d.%m")

    # Save the user's reply as the waking up time for the current activity
    context.user_data["schedule"][f"{current_date}_day_rate"] = update.message.text
    add_to_json(context.user_data)

    # Move to the state for saving waking up time
    return SHOW_DAY_STATS


async def show_day_stats(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    await context.bot.send_message(user_id, "Здесь будет статистика за день")

    return GET_SCHEDULE


async def get_end_night_sleep_time(update: Update, context: CallbackContext) -> int:
    # Ask about waking up time after night
    await update.message.reply_text(f"Во сколько вы проснулись cегодня утром ?")

    current_date = datetime.now().strftime("%d.%m")

    # Save the user's reply
    context.user_data["schedule"][
        f"{current_date}_end_night_sleep"
    ] = update.message.text
    add_to_json(context.user_data)

    return GET_NIGHT_RATING


async def get_night_rating(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(f"Оцените сегодняшнюю ночь от 1 до 10")

    current_date = datetime.now().strftime("%d.%m")

    # Save the user's reply as the waking up time for the current activity
    context.user_data["schedule"][f"{current_date}_night_rate"] = update.message.text
    add_to_json(context.user_data)

    # Move to the state for saving waking up time
    return SHOW_NIGHT_STATS


async def show_night_stats(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    await context.bot.send_message(
        user_id, "Здесь будет статистика за ночь и рекомендации на день"
    )

    return GET_SCHEDULE


async def get_fall_asleep_time(update: Update, context: CallbackContext) -> int:
    i = context.user_data.get("activity_count", 1)
    current_date = datetime.now().strftime("%d.%m")
    await update.message.reply_text(f"Когда вы уснули в {i} раз?")
    # Save the response to the falling asleep time question
    print(context.user_data)
    context.user_data["schedule"][
        f"{current_date}_{i - 1}fall_asleep_time"
    ] = update.message.text

    add_to_json(context.user_data)

    return GET_WAKE_UP_TIME


async def get_wake_up_time(update: Update, context: CallbackContext) -> int:
    i = context.user_data.get("activity_count", 1)
    user_id = update.message.from_user.id
    await context.bot.send_message(user_id, f"{i} бодрствование.")

    # Ask about waking up time for the current activity
    await update.message.reply_text(f"Во сколько вы проснулись в {i} раз за день?")

    current_date = datetime.now().strftime("%d.%m")

    # Save the user's reply as the waking up time for the current activity
    context.user_data["schedule"][
        f"{current_date}_{i}wake_up_time"
    ] = update.message.text
    save_sleep_duration(context.user_data, i)
    add_to_json(context.user_data)

    # Move to the state for saving waking up time
    return GET_SCHEDULE


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END


# You can add more states and corresponding functions for additional questions (GET_ANSWER_2, GET_ANSWER_3, etc.)

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_command),
        CommandHandler("daysleep", get_fall_asleep_time),
        CommandHandler("endnightsleep", get_end_night_sleep_time),
        CommandHandler("startnightsleep", get_start_night_sleep_time),
    ],
    states={
        GET_USER_PROBLEM: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_problem)
        ],
        GET_CHILD_GENDER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_child_gender)
        ],
        GET_CHILD_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_child_name)
        ],
        GET_CHILD_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_child_age)],
        GET_FOODTYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_foodtype)],
        GET_USER_PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_phone)
        ],
        GET_USER_EMAIL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_email)
        ],
        GET_SCHEDULE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_schedule),
            CommandHandler("daysleep", get_fall_asleep_time),
        ],
        GET_FALL_ASLEEP_TIME: [CommandHandler("daysleep", get_fall_asleep_time)],
        GET_WAKE_UP_TIME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_wake_up_time)
        ],
        GET_START_NIGHT_SLEEP: [
            CommandHandler("startnightsleep", get_start_night_sleep_time)
        ],
        GET_DAY_RATING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_day_rating)
        ],
        SHOW_DAY_STATS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_day_stats)
        ],
        GET_END_NIGHT_SLEEP: [
            CommandHandler("endnightsleep", get_end_night_sleep_time)
        ],
        GET_NIGHT_RATING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_night_rating)
        ],
        SHOW_NIGHT_STATS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_night_stats)
        ],
        # Add states for additional questions here
    },
    fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
)

# Assuming 'application' is the instance of your Telegram bot application


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6726344922:AAHq2Rd3k4BjdTow9-rB8Nr1e7tp9PMfSRc")
        .build()
    )

    application.add_handler(conversation_handler)
    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start_command))

    print("Бот пошел")
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
