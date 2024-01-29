from datetime import datetime


def calculate_time_difference(start: str, end: str) -> int:
    # Define the time format for parsing
    start_time: datetime = datetime.strptime(start, "%H:%M")
    end_time: datetime = datetime.strptime(end, "%H:%M")

    if end_time < start_time:
        end_time = end_time.replace(
            day=end_time.day + 1
        )  # Move end time to the next day

    hour_difference = (
        end_time - start_time
    ).total_seconds() / 60  # Convert total seconds to hours
    return int(hour_difference)
