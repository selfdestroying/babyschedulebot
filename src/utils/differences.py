from datetime import datetime


def calculate_minutes_difference(start: str, end: str) -> int:
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


# def calculate_minutes_difference(start_time, end_time):
#     # Define the time format for parsing
#     time_format = "%H:%M"

#     # Convert the time strings to datetime objects
#     start_time = datetime.strptime(start_time, time_format)
#     end_time = datetime.strptime(end_time, time_format)

#     # Calculate the time difference
#     time_difference = end_time - start_time

#     # Extract the total seconds and convert to hours and minutes
#     total_seconds = time_difference.total_seconds()
#     hours = int(total_seconds // 3600)
#     minutes = int((total_seconds % 3600) // 60)
#     total_minutes = int(time_difference.total_seconds() / 60)

#     # Return the time difference as a tuple (hours, minutes)
#     return total_minutes


def get_days_in_month(month, year):
    # Returns the number of days in a given month and year
    if month == 2:  # February
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29  # Leap year
        else:
            return 28
    elif month in [4, 6, 9, 11]:  # April, June, September, November
        return 30
    else:
        return 31


def calculate_child_age_in_months(birth_date):
    current_date = datetime.today()
    years = current_date.year - birth_date.year
    months = current_date.month - birth_date.month
    days = current_date.day - birth_date.day

    # Adjust for negative differences
    if days < 0:
        months -= 1
        days += get_days_in_month(birth_date.month, birth_date.year)
    if months < 0:
        years -= 1
        months += 12

    return months + years * 12
