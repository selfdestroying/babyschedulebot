import json
from datetime import datetime

idealdata = {
    "1": {
        "day": {
            "sleep": {
                "total": [300, 420],  # сумма всех дневных снов
                "average_duration": [20, 180],  # продолжительность одного сна
                "amount": [4, 6],  # количество снов днём
            },
            "activity": {
                "total": [420, 600],  # сумма всего времени бодрствования
                "average_duration": [70, 80],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [480, 600],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [840, 1020],  # все дневные сны + ночной сон
    },
    "2": {
        "day": {
            "sleep": {
                "total": [300, 420],  # сумма всех дневных снов
                "average_duration": [20, 180],  # продолжительность одного сна
                "amount": [4, 6],  # количество снов днём
            },
            "activity": {
                "total": [420, 600],  # сумма всего времени бодрствования
                "average_duration": [70, 80],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [480, 600],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [840, 1020],  # все дневные сны + ночной сон
    },
    "3": {
        "day": {
            "sleep": {
                "total": [300, 420],  # сумма всех дневных снов
                "average_duration": [20, 180],  # продолжительность одного сна
                "amount": [4, 6],  # количество снов днём
            },
            "activity": {
                "total": [420, 600],  # сумма всего времени бодрствования
                "average_duration": [80, 105],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [480, 600],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [840, 1020],  # все дневные сны + ночной сон
    },
    "4": {
        "day": {
            "sleep": {
                "total": [210, 270],  # сумма всех дневных снов
                "average_duration": [40, 90],  # продолжительность одного сна
                "amount": [3, 4],  # количество снов днём
            },
            "activity": {
                "total": [570, 630],  # сумма всего времени бодрствования
                "average_duration": [105, 115],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [600, 660],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [810, 870],  # все дневные сны + ночной сон
    },
    "5": {
        "day": {
            "sleep": {
                "total": [210, 270],  # сумма всех дневных снов
                "average_duration": [40, 90],  # продолжительность одного сна
                "amount": [3, 4],  # количество снов днём
            },
            "activity": {
                "total": [570, 630],  # сумма всего времени бодрствования
                "average_duration": [110, 135],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [600, 660],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [810, 870],  # все дневные сны + ночной сон
    },
    "6": {
        "day": {
            "sleep": {
                "total": [180, 210],  # сумма всех дневных снов
                "average_duration": [40, 90],  # продолжительность одного сна
                "amount": 3,  # количество снов днём
            },
            "activity": {
                "total": [615, 660],  # сумма всего времени бодрствования
                "average_duration": [150, 165],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [600, 660],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [780, 825],  # все дневные сны + ночной сон
    },
    "7": {
        "day": {
            "sleep": {
                "total": [180, 210],  # сумма всех дневных снов
                "average_duration": [40, 90],  # продолжительность одного сна
                "amount": [3, 3],  # количество снов днём
            },
            "activity": {
                "total": [630, 660],  # сумма всего времени бодрствования
                "average_duration": [150, 165],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [600, 660],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [3, 4],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [780, 825],  # все дневные сны + ночной сон
    },
    "8": {
        "day": {
            "sleep": {
                "total": [150, 210],  # сумма всех дневных снов
                "average_duration": [40, 90],  # продолжительность одного сна
                "amount": [2, 3],  # количество снов днём
            },
            "activity": {
                "total": [630, 690],  # сумма всего времени бодрствования
                "average_duration": [165, 210],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [600, 660],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [2, 3],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [750, 810],  # все дневные сны + ночной сон
    },
    "9": {
        "day": {
            "sleep": {
                "total": [150, 210],  # сумма всех дневных снов
                "average_duration": [40, 90],  # продолжительность одного сна
                "amount": [2, 3],  # количество снов днём
            },
            "activity": {
                "total": [630, 690],  # сумма всего времени бодрствования
                "average_duration": [165, 210],  # продолжительность 1 бодрствования
            },
            "feeding": {},  # особенности питания. пока не заморчаиваемся. сделаем позже
        },
        "night": {
            "total": [600, 660],  # продолжительность ночного сна
            "feedings": {  # количество кормлений за ночь, в зависимости от типа кормаления
                "breast": [2, 3],  # грудное вскармливание
                "formula": [1, 2],  # смесь
            },
        },
        "SLEEPS_ALL": [750, 810],  # все дневные сны + ночной сон
    },
    "10": {
        "total_day_sleep": 100,
        "total_day_activity": 100,
        "total_night_sleep": 100,
    },
    "11": {
        "total_day_sleep": 100,
        "total_day_activity": 100,
        "total_night_sleep": 100,
    },
    "12": {
        "total_day_sleep": 100,
        "total_day_activity": 100,
        "total_night_sleep": 100,
    },
}


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


# создать список с бодрствованиями после того, как введены данные про начало и конец ночного сна и все дневные сны
def get_activity(user_data):
    date = "28.01"
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
                "activity_duration": calculate_time_difference(wake_up, fall_asleep),
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
            "activity_duration": calculate_time_difference(wake_up, fall_asleep),
        }
    )
    user_data["schedule"][date]["day_activities"] = activity_list


# сумма всех бодрствований
def get_total_day_activity(user_data):
    date = "28.01"
    day_activities = user_data["schedule"][date]["day_activities"]
    total_duration = []
    for i in range(len(day_activities)):
        total_duration.append(day_activities[i]["activity_duration"])
    user_data["schedule"][date]["TOTAL_DAY_ACTIVITY"] = sum(total_duration)


# сумма всех дневных снов
def get_total_day_sleep(user_data):
    date = "28.01"
    day_sleeps = user_data["schedule"][date]["sleeps"]
    total_duration = []
    for i in range(len(day_sleeps)):
        total_duration.append(day_sleeps[i]["sleep_duration"])
    user_data["schedule"][date]["TOTAL_DAY_SLEEP"] = sum(total_duration)


# сумма ночного сна и всех дневных
def get_sleeps_all(user_data):
    date = "28.01"
    day = user_data["schedule"][date]["TOTAL_DAY_SLEEP"]
    night = user_data["schedule"][date]["night_duration"]
    user_data["schedule"][date]["SLEEPS_ALL"] = day + night


# сравнить каждый дневной сон с эталоном
def compare_day_sleeps(user_data, idealdata):
    date = "28.01"
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
def compare_day_activity(user_data, idealdata):
    date = "28.01"
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
def compare_total_day_sleep(user_data, idealdata):
    date = "28.01"
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
def compare_total_day_activity(user_data, idealdata):
    date = "28.01"
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
def compare_sleep_all(user_data, idealdata):
    date = "28.01"
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
def compare_total_night_sleep(user_data, idealdata):
    date = "28.01"
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
def compare_day_sleep_amount(user_data, idealdata):
    date = "28.01"
    child_age = user_data["child"]["age"]

    n_min = idealdata[child_age]["day"]["sleep"]["amount"][0]
    n_max = idealdata[child_age]["day"]["sleep"]["amount"][1]
    n = len(user_data["schedule"][date]["day_activities"])
    if n >= n_min and n <= n_max:
        return f"Всего дневных снов: {n}. Это норма"
    elif n < n_min:
        return f"Всего дневных снов: {n}. Это короче чем нужно"
    elif n > n_max:
        return f"Всего дневных снов: {n}. Это больше чем нужно"


def get_recomendation(id):
    with open("newjsonfrombot.json", "r") as file:
        users = json.load(file)
        user_data = users[id]
    get_activity(user_data)
    get_total_day_activity(user_data)
    get_total_day_sleep(user_data)
    get_sleeps_all(user_data)
    x = (
        compare_day_sleeps(user_data, idealdata)
        + "\n"
        + compare_day_sleep_amount(user_data, idealdata)
        + "\n"
        + compare_total_day_sleep(user_data, idealdata)
        + "\n"
        + compare_total_night_sleep(user_data, idealdata)
        + "\n"
        + compare_sleep_all(user_data, idealdata)
        + "\n"
        + compare_day_activity(user_data, idealdata)
        + "\n"
        + compare_total_day_activity(user_data, idealdata)
    )
    users[id] = user_data
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(users, json_file, ensure_ascii=False, indent=4)
    print("ВСЁ")
    return x
