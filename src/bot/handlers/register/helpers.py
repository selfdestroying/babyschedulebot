from datetime import datetime

import pytz

from src.api.dbapi import childapi, scheduleapi, userapi
from src.utils.differences import calculate_minutes_difference


def register_user(data: dict[str, any]):
    id = data.get("id")
    user_name = data.get("user_name")
    user_phone = data.get("user_phone")
    user_email = data.get("user_email")
    user_problem = data.get("user_problem")
    userapi.create(
        id=id,
        name=user_name,
        phone=user_phone,
        email=user_email,
        problem=user_problem,
    )


def register_child(data: dict[str, any]):
    id = data.get("id")
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    child_birth_date = data.get("child_birth_date")
    food_type = data.get("food_type")
    child_age = data.get("child_age")
    childapi.create(
        name=child_name,
        gender=child_gender,
        birth_date=child_birth_date,
        age=child_age,
        food_type=food_type,
        user_id=id,
    )


def register_schedule(data: dict[str, any]):
    current_date = datetime.now(pytz.timezone("Etc/GMT-3"))
    id = data.get("id")
    start_night_time = data.get("start_night_time")
    end_night_time = data.get("end_night_time")
    night_wake_up_count = data.get("night_wake_up_count")
    night_rating = data.get("night_rating")
    night_duration = calculate_minutes_difference(start_night_time, end_night_time)
    scheduleapi.create(
        user_id=id,
        date=current_date.strftime("%Y-%m-%d"),
        start_day=end_night_time,
        start_prev_night=start_night_time,
        night_duration=night_duration,
        night_rating=night_rating,
        night_wake_up_count=night_wake_up_count,
    )
