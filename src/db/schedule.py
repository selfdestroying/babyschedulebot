import json
import datetime

from models.DayInfo import DayInfo


def write_day_info(id: str, day_info: DayInfo) -> None:
    with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
        user_data = json.load(json_file)
    current_date = datetime.datetime.now().strftime("%d.%m")
    user_data[id]["schedule"][current_date] = day_info.model_dump()
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(user_data, json_file, indent=4)


def add_sleep(id: str, sleep: dict) -> None:
    with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
        user_data = json.load(json_file)
        current_date = datetime.datetime.now().strftime("%d.%m")
        if current_date not in user_data[id]["schedule"].keys():
            user_data[id]["schedule"][current_date]["sleeps"] = [sleep]
        else:
            user_data[id]["schedule"][current_date]["sleeps"].append(sleep)
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)
