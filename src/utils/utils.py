from datetime import datetime


def calculate_time_difference(start_time, end_time):
    # Define the time format for parsing
    start_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")

    if end_time < start_time:
        end_time = end_time.replace(
            day=end_time.day + 1
        )  # Move end time to the next day

    hour_difference = (
        end_time - start_time
    ).total_seconds() / 60  # Convert total seconds to hours
    return hour_difference
