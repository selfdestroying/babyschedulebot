from datetime import datetime, timedelta


def convert_minutes_to_hours_and_minutes(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}:{remaining_minutes:02d}"


def calculate_time_to_remind(
    wake_up_time: str, message_send_time: str, average_activity_duration: list
) -> int | None:
    """
    Calculate the time to remind based on the wake up time, message send time, and ideal sleep duration.

    Parameters:
    - wake_up_time: str
    - message_send_time: str
    - ideal_sleep_duration: list

    Returns:
    - int or None
    """
    average_activity_duration_min = average_activity_duration[0]
    average_activity_duration_max = average_activity_duration[1]

    average_activity_duration_min_hours = convert_minutes_to_hours_and_minutes(
        average_activity_duration_min
    )
    average_activity_duration_max_hours = convert_minutes_to_hours_and_minutes(
        average_activity_duration_max
    )

    wake_up_time_dt = datetime.strptime(wake_up_time, "%H:%M:%S")
    message_send_time_dt = datetime.strptime(message_send_time, "%H:%M:%S")

    next_fall_asleep_time_min_dt = wake_up_time_dt + timedelta(
        minutes=average_activity_duration_min
    )
    next_fall_asleep_time_max_dt = wake_up_time_dt + timedelta(
        minutes=average_activity_duration_max
    )
    if message_send_time_dt < next_fall_asleep_time_max_dt:
        time_to_remind_dt: timedelta = (
            next_fall_asleep_time_max_dt - message_send_time_dt
        )
        return {
            "time_to_remind": time_to_remind_dt.seconds,
            "activity_duration_min": average_activity_duration_min_hours,
            "activity_duration_max": average_activity_duration_max_hours,
            "next_fall_asleep_time_min": next_fall_asleep_time_min_dt.strftime("%H:%M"),
            "next_fall_asleep_time_max": next_fall_asleep_time_max_dt.strftime("%H:%M"),
        }
    else:
        return None
