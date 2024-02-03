import datetime
import json

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
        user_data[id]["schedule"][current_date]["sleeps"].append(sleep)
        user_data[id]["schedule"][current_date]["sleeps"].sort(
            key=lambda x: x["start_sleep_time"]
        )

    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)
