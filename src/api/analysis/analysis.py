# создать список с бодрствованиями после того, как введены данные про начало и конец ночного сна и все дневные сны
import json
from datetime import datetime

from src.api.analysis.ideal_data import idealdata
from src.utils.differences import calculate_minutes_difference


def get_activity(user_data, date):
    day_sleeps = user_data["schedule"][date]["sleeps"]

    activity_list = []

    for i in range(len(day_sleeps)):
        if i == 0:
            wake_up = user_data["schedule"][date]["end_night_sleep_time"]
            fall_asleep = day_sleeps[i]["start_sleep_time"]
        else:
            wake_up = day_sleeps[i - 1]["end_sleep_time"]
            fall_asleep = day_sleeps[i]["start_sleep_time"]
        activity_list.append(
            {
                "start_activity_time": wake_up,
                "end_activity_time": fall_asleep,
                "activity_duration": calculate_minutes_difference(wake_up, fall_asleep),
            }
        )
    wake_up = user_data["schedule"][date]["sleeps"][len(day_sleeps) - 1][
        "end_sleep_time"
    ]
    fall_asleep = user_data["schedule"][date]["start_night_sleep_time"]
    activity_list.append(
        {
            "start_activity_time": wake_up,
            "end_activity_time": fall_asleep,
            "activity_duration": calculate_minutes_difference(wake_up, fall_asleep),
        }
    )
    user_data["schedule"][date]["day_activities"] = activity_list


# сумма всех бодрствований
def get_total_day_activity(user_data, date):
    day_activities = user_data["schedule"][date]["day_activities"]
    total_duration = []
    for i in range(len(day_activities)):
        total_duration.append(day_activities[i]["activity_duration"])
    user_data["schedule"][date]["TOTAL_DAY_ACTIVITY"] = sum(total_duration)


# сумма всех дневных снов
def get_total_day_sleep(user_data, date):
    day_sleeps = user_data["schedule"][date]["sleeps"]
    total_duration = []
    for i in range(len(day_sleeps)):
        total_duration.append(day_sleeps[i]["sleep_duration"])
    user_data["schedule"][date]["TOTAL_DAY_SLEEP"] = sum(total_duration)


# сумма ночного сна и всех дневных
def get_sleeps_all(user_data, date):
    day = user_data["schedule"][date]["TOTAL_DAY_SLEEP"]
    night = user_data["schedule"][date]["night_duration"]
    user_data["schedule"][date]["SLEEPS_ALL"] = day + night


# сравнить каждый дневной сон с эталоном
def compare_day_sleeps(user_data, idealdata, date):
    child_age = user_data["child"]["age"]
    day_sleeps = user_data["schedule"][date]["sleeps"]
    n_min = idealdata[child_age]["day"]["sleep"]["average_duration"][0]
    n_max = idealdata[child_age]["day"]["sleep"]["average_duration"][1]
    result = "АНАЛИЗ ДНЕВНОГО СНА\n"
    for i in range(len(day_sleeps)):
        n = day_sleeps[i]["sleep_duration"]
        if n >= n_min and n <= n_max:
            result += f"Ваш {i+1} сон длился {n} минут. Это норма\n"
        elif n < n_min:
            result += f"Ваш {i+1} сон длился {n} минут. Это короче чем нужно\n"
        elif n > n_max:
            result += f"Ваш {i+1} сон длился {n} минут. Это дольше чем нужно\n"
    return result


# сравнить каждое бодрствование с эталоном
def compare_day_activity(user_data, idealdata, date):
    child_age = user_data["child"]["age"]
    day_activities = user_data["schedule"][date]["day_activities"]
    n_min = idealdata[child_age]["day"]["activity"]["average_duration"][0]
    n_max = idealdata[child_age]["day"]["activity"]["average_duration"][1]
    result = "АНАЛИЗ БОДРСТВОВАНИЯ\n"
    for i in range(len(day_activities)):
        n = day_activities[i]["activity_duration"]
        if n >= n_min and n <= n_max:
            result += f"Ваше {i+1} бодрствование длилось {n} минут. Это норма\n"
        elif n < n_min:
            result += (
                f"Ваше {i+1} бодрствование длилось {n} минут. Это короче чем нужно\n"
            )
        elif n > n_max:
            result += (
                f"Ваше {i+1} бодрствование длилось {n} минут. Это дольше чем нужно\n"
            )
    return result


# сравнить сумму всех снов в течение дня с эталоном
def compare_total_day_sleep(user_data, idealdata, date):
    child_age = user_data["child"]["age"]

    n_min = idealdata[child_age]["day"]["sleep"]["total"][0]
    n_max = idealdata[child_age]["day"]["sleep"]["total"][1]
    n = user_data["schedule"][date]["TOTAL_DAY_SLEEP"]
    if n >= n_min and n <= n_max:
        return f"Всего дневного сна: {n} минут. Это норма"
    elif n < n_min:
        return f"Всего дневного сна: {n} минут. Это короче чем нужно"
    elif n > n_max:
        return f"Всего дневного сна: {n} минут. Это больше чем нужно"


# сравнить сумму всего бодрствования с эталоном
def compare_total_day_activity(user_data, idealdata, date):
    child_age = user_data["child"]["age"]

    n_min = idealdata[child_age]["day"]["activity"]["total"][0]
    n_max = idealdata[child_age]["day"]["activity"]["total"][1]
    n = user_data["schedule"][date]["TOTAL_DAY_ACTIVITY"]
    if n >= n_min and n <= n_max:
        return f"Всего бодрствования: {n} минут. Это норма"
    elif n < n_min:
        return f"Всего бодрствования: {n} минут. Это короче чем нужно"
    elif n > n_max:
        return f"Всего бодрствования: {n} минут. Это больше чем нужно"


# сравнить сумму всех снов за сутки (день+ночь) с эталоном
def compare_sleep_all(user_data, idealdata, date):
    child_age = user_data["child"]["age"]

    n_min = idealdata[child_age]["SLEEPS_ALL"][0]
    n_max = idealdata[child_age]["SLEEPS_ALL"][1]
    n = user_data["schedule"][date]["SLEEPS_ALL"]
    if n >= n_min and n <= n_max:
        return f"Всего сна: {n} минут. Это норма"
    elif n < n_min:
        return f"Всего сна: {n} минут. Это короче чем нужно"
    elif n > n_max:
        return f"Всего сна: {n} минут. Это больше чем нужно"


# сравнить ночной сон с эталоном
def compare_total_night_sleep(user_data, idealdata, date):
    child_age = user_data["child"]["age"]

    n_min = idealdata[child_age]["night"]["total"][0]
    n_max = idealdata[child_age]["night"]["total"][1]
    n = user_data["schedule"][date]["night_duration"]
    if n >= n_min and n <= n_max:
        return f"Всего ночного сна: {n} минут. Это норма"
    elif n < n_min:
        return f"Всего ночного сна: {n} минут. Это короче чем нужно"
    elif n > n_max:
        return f"Всего ночного сна: {n} минут. Это больше чем нужно"


# сравнить количество дневных снов с эталоном
def compare_day_sleep_amount(user_data, idealdata, date):
    child_age = user_data["child"]["age"]

    n_min = idealdata[child_age]["day"]["sleep"]["amount"][0]
    n_max = idealdata[child_age]["day"]["sleep"]["amount"][1]
    n = len(user_data["schedule"][date]["sleeps"])
    if n >= n_min and n <= n_max:
        return f"Всего дневных снов: {n}. Это норма"
    elif n < n_min:
        return f"Всего дневных снов: {n}. Это короче чем нужно"
    elif n > n_max:
        return f"Всего дневных снов: {n}. Это больше чем нужно"


def get_recomendation(id):
    try:
        with open("newjsonfrombot.json", "r", encoding="UTF-8") as file:
            users = json.load(file)
            user_data = users[id]
        current_date = datetime.now().strftime("%d.%m")
        error_message = ""
        if current_date not in user_data["schedule"]:
            error_message += "\nНет данных о сегодняшнем дне"
        if (
            "start_night_sleep_time" not in user_data["schedule"][current_date]
            or "end_night_sleep_time" not in user_data["schedule"][current_date]
        ):
            error_message += "\nНет данных о ночном сне"
        if len(user_data["schedule"][current_date]["sleeps"]) == 0:
            error_message += "\nНет данных о дневных снах"

        if error_message:
            return "Недостаточно данных для анализа:" + error_message
        get_activity(user_data, current_date)
        get_total_day_activity(user_data, current_date)
        get_total_day_sleep(user_data, current_date)
        get_sleeps_all(user_data, current_date)
        x = (
            compare_day_sleeps(user_data, idealdata, current_date)
            + "\n"
            + compare_day_sleep_amount(user_data, idealdata, current_date)
            + "\n"
            + compare_total_day_sleep(user_data, idealdata, current_date)
            + "\n"
            + compare_total_night_sleep(user_data, idealdata, current_date)
            + "\n"
            + compare_sleep_all(user_data, idealdata, current_date)
            + "\n"
            + compare_day_activity(user_data, idealdata, current_date)
            + "\n"
            + compare_total_day_activity(user_data, idealdata, current_date)
        )
        users[id] = user_data
        with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
            json.dump(users, json_file, ensure_ascii=False, indent=4)
        return x
    except KeyError:
        return "Недостаточно даннах для анализа"
