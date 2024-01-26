from datetime import datetime


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
