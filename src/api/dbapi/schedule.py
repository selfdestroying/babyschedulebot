from postgrest.exceptions import APIError

from src.api.dbapi.database import supabase


def create(
    user_id,
    date: str,
    start_day: str,
    start_prev_night: str,
    night_duration: int,
    night_rating: int,
    night_wake_up_count: int,
) -> bool:
    try:
        response = (
            supabase.table("schedules")
            .insert(
                {
                    "id": user_id,
                    "user_id": user_id,
                    "date": date,
                    "start_day": start_day,
                    "start_prev_night": start_prev_night,
                    "night_duration": night_duration,
                    "night_rating": night_rating,
                    "night_wake_up_count": night_wake_up_count,
                }
            )
            .execute()
        )
        return True
    except (IndexError, APIError) as error:
        print(error)
        return False


def read(user_id: int, date: str) -> dict | list:
    try:
        response = (
            supabase.table("schedules")
            .select("*")
            .eq("user_id", user_id)
            .eq("date", date)
            .execute()
        )
        return response.data[0]
    except IndexError:
        return {}


def update(id, date: str, payload: dict):
    try:
        response = (
            supabase.table("schedules")
            .update(payload)
            .eq("user_id", id)
            .eq("date", date)
            .execute()
        )
        return response.data[0]
    except IndexError:
        return []


def update_sleeps(user_id: int, date: str, sleep: dict):
    try:
        sleeps = (
            supabase.table("schedules")
            .select("sleeps")
            .eq("user_id", user_id)
            .eq("date", date)
            .execute()
        ).data[0]["sleeps"]
        sleeps.append(sleep)
        sleeps.sort(key=lambda x: x["start_sleep_time"])
        response = (
            supabase.table("schedules")
            .update({"sleeps": sleeps})
            .eq("user_id", user_id)
            .eq("date", date)
            .execute()
        )
        return response.data[0]
    except IndexError:
        return []


def delete(user_id: int, date: str) -> dict | list:
    supabase.table("schedules").delete().eq("user_id", user_id).eq(
        "date", date
    ).execute()
