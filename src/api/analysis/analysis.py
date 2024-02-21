# создать список с бодрствованиями после того, как введены данные про начало и конец ночного сна и все дневные сны

from src.api.analysis.ideal_data import ideal_data
from src.utils.differences import calculate_minutes_difference


# activities
def get_activity(schedule: dict, end_day_time: str = None):
    sleeps = schedule["sleeps"]
    activity_list = []

    wake_up = schedule["start_day"]
    fall_asleep = sleeps[0]["start_sleep_time"]
    activity_list.append(
        {
            "start_activity_time": wake_up,
            "end_activity_time": fall_asleep,
            "activity_duration": calculate_minutes_difference(wake_up, fall_asleep),
        }
    )
    for i in range(1, len(sleeps)):
        wake_up = sleeps[i - 1]["end_sleep_time"]
        fall_asleep = sleeps[i]["start_sleep_time"]
        activity_list.append(
            {
                "start_activity_time": wake_up,
                "end_activity_time": fall_asleep,
                "activity_duration": calculate_minutes_difference(wake_up, fall_asleep),
            }
        )

    wake_up = sleeps[-1]["end_sleep_time"]
    activity_list.append(
        {
            "start_activity_time": wake_up,
            "end_activity_time": end_day_time if end_day_time else schedule["end_day"],
            "activity_duration": calculate_minutes_difference(
                wake_up, end_day_time if end_day_time else schedule["end_day"]
            ),
        }
    )
    return activity_list


# сумма всех бодрствований total_day_activity
def get_total_day_activity(day_activities: list):
    total_duration = []
    for i in range(len(day_activities)):
        total_duration.append(day_activities[i]["activity_duration"])
    return sum(total_duration)


# сумма всех дневных снов total_day_sleep
def get_total_day_sleep(sleeps):
    total_duration = []
    for i in range(len(sleeps)):
        total_duration.append(sleeps[i]["sleep_duration"])
    return sum(total_duration)


# сумма ночного сна и всех дневных sleeps_all
def get_sleeps_all(total_day_sleep, night_duration):
    return total_day_sleep + night_duration


# сравнить каждый дневной сон с эталоном
def compare_day_sleeps(sleeps: list, age: int, idealdata: dict):
    n_min = idealdata[age]["day"]["sleep"]["average_duration"][0]
    n_max = idealdata[age]["day"]["sleep"]["average_duration"][1]
    result = ""
    for i in range(len(sleeps)):
        n = sleeps[i]["sleep_duration"]
        if n >= n_min and n <= n_max:
            result += f"Ваш {i+1} сон длился {n} минут. Это норма\n"
        elif n < n_min:
            result += f"Ваш {i+1} сон длился {n} минут. Это короче чем нужно\n"
        elif n > n_max:
            result += f"Ваш {i+1} сон длился {n} минут. Это дольше чем нужно\n"
    return result


def compare_day_sleep(sleeps: list, age: int, idealdata: dict):
    n_min = idealdata[age]["day"]["sleep"]["average_duration"][0]
    n_max = idealdata[age]["day"]["sleep"]["average_duration"][1]
    result = ""
    n = sleeps[0]["sleep_duration"]
    if n >= n_min and n <= n_max:
        result += f"Ваш сон длился {n} минут. Это норма\n"
    elif n < n_min:
        result += f"Ваш сон длился {n} минут. Это короче чем нужно\n"
    elif n > n_max:
        result += f"Ваш сон длился {n} минут. Это дольше чем нужно\n"
    return result


# сравнить каждое бодрствование с эталоном
def compare_day_activities(activities: list, age: int, idealdata: dict):
    n_min = idealdata[age]["day"]["activity"]["average_duration"][0]
    n_max = idealdata[age]["day"]["activity"]["average_duration"][1]
    result = ""
    for i in range(len(activities)):
        n = activities[i]["activity_duration"]
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
def compare_total_day_sleep(total_day_sleep: int, age: int, idealdata: dict):
    n_min = idealdata[age]["day"]["sleep"]["total"][0]
    n_max = idealdata[age]["day"]["sleep"]["total"][1]
    if total_day_sleep >= n_min and total_day_sleep <= n_max:
        return f"Всего дневного сна: {total_day_sleep} минут. Это норма"
    elif total_day_sleep < n_min:
        return f"Всего дневного сна: {total_day_sleep} минут. Это короче чем нужно"
    else:
        return f"Всего дневного сна: {total_day_sleep} минут. Это больше чем нужно"


# сравнить сумму всего бодрствования с эталоном
def compare_total_day_activity(total_day_activity: int, age: int, idealdata: dict):
    n_min = idealdata[age]["day"]["activity"]["total"][0]
    n_max = idealdata[age]["day"]["activity"]["total"][1]
    if total_day_activity >= n_min and total_day_activity <= n_max:
        return f"Всего бодрствования: {total_day_activity} минут. Это норма"
    elif total_day_activity < n_min:
        return f"Всего бодрствования: {total_day_activity} минут. Это короче чем нужно"
    else:
        return f"Всего бодрствования: {total_day_activity} минут. Это больше чем нужно"


# сравнить сумму всех снов за сутки (день+ночь) с эталоном
def compare_sleeps_all(sleeps_all: int, age: int, idealdata: dict):
    n_min = idealdata[age]["SLEEPS_ALL"][0]
    n_max = idealdata[age]["SLEEPS_ALL"][1]
    if sleeps_all >= n_min and sleeps_all <= n_max:
        return f"Всего сна: {sleeps_all} минут. Это норма"
    elif sleeps_all < n_min:
        return f"Всего сна: {sleeps_all} минут. Это короче чем нужно"
    else:
        return f"Всего сна: {sleeps_all} минут. Это больше чем нужно"


# сравнить ночной сон с эталоном
def compare_total_night_sleep(night_duration: int, age: int, idealdata: dict):
    n_min = idealdata[age]["night"]["total"][0]
    n_max = idealdata[age]["night"]["total"][1]
    if night_duration >= n_min and night_duration <= n_max:
        return f"Всего ночного сна: {night_duration} минут. Это норма"
    elif night_duration < n_min:
        return f"Всего ночного сна: {night_duration} минут. Это короче чем нужно"
    else:
        return f"Всего ночного сна: {night_duration} минут. Это больше чем нужно"


# сравнить количество дневных снов с эталоном
def compare_day_sleep_amount(sleeps: list, age: int, idealdata: dict):
    n_min = idealdata[age]["day"]["sleep"]["amount"][0]
    n_max = idealdata[age]["day"]["sleep"]["amount"][1]
    n = len(sleeps)
    if n >= n_min and n <= n_max:
        return f"Всего дневных снов: {n}. Это норма"
    elif n < n_min:
        return f"Всего дневных снов: {n}. Это короче чем нужно"
    else:
        return f"Всего дневных снов: {n}. Это больше чем нужно"


def get_recomendation(age: int, schedule: dict):
    text_message = ""
    end_day_time = schedule["end_day"]
    sleeps = schedule["sleeps"]
    night_duration = schedule["night_duration"]

    day_activities = get_activity(schedule=schedule, end_day_time=end_day_time)
    total_day_activity = get_total_day_activity(day_activities=day_activities)
    total_day_sleep = get_total_day_sleep(sleeps=sleeps)
    sleeps_all = get_sleeps_all(
        total_day_sleep=total_day_sleep, night_duration=night_duration
    )

    day_sleeps_result = compare_day_sleeps(sleeps=sleeps, age=age, idealdata=ideal_data)

    day_sleep_amoun_result = compare_day_sleep_amount(
        sleeps=sleeps, age=age, idealdata=ideal_data
    )

    total_day_sleep_result = compare_total_day_sleep(
        total_day_sleep=total_day_sleep, age=age, idealdata=ideal_data
    )

    total_night_sleep_result = compare_total_night_sleep(
        night_duration=night_duration, age=age, idealdata=ideal_data
    )

    sleep_all = compare_sleeps_all(sleeps_all=sleeps_all, age=age, idealdata=ideal_data)

    day_activities_result = compare_day_activities(
        activities=day_activities, age=age, idealdata=ideal_data
    )

    total_day_activity_result = compare_total_day_activity(
        total_day_activity=total_day_activity, age=age, idealdata=ideal_data
    )

    data = {
        "activities": day_activities,
        "total_day_activity": total_day_activity,
        "total_day_sleep": total_day_sleep,
        "sleeps_all": sleeps_all,
    }
    text_message = f"<b>АНАЛИЗ ДНЕВНОГО СНА\n</b>\n{day_sleeps_result}\n{day_sleep_amoun_result}\n{total_day_sleep_result}\n{total_night_sleep_result}\n{sleep_all}\n{day_activities_result}\n{total_day_activity_result}"

    return data, text_message
