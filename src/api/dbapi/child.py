from src.api.dbapi.database import supabase


def create(
    name: str,
    gender: str,
    birth_date: str,
    age: int,
    food_type: str,
    user_id: int,
) -> dict | list:
    try:
        response = (
            supabase.table("childs")
            .insert(
                {
                    "name": name,
                    "gender": gender,
                    "birth_date": birth_date,
                    "age": age,
                    "food_type": food_type,
                    "user_id": user_id,
                }
            )
            .execute()
        )
        return response.data[0]
    except IndexError:
        return []


def read(user_id: int) -> list:
    try:
        response = supabase.table("childs").select("*").eq("user_id", user_id).execute()

        return response.data
    except IndexError:
        return []


def update(
    name: str = None,
    gender: str = None,
    birth_date: str = None,
    age: int = None,
    food_type: str = None,
    user_id: int = None,
) -> dict | list:
    try:
        data = {}
        if name:
            data["name"] = name
        if gender:
            data["gender"] = gender
        if birth_date:
            data["birth_date"] = birth_date
        if age:
            data["age"] = age
        if food_type:
            data["food_type"] = food_type
        response = (
            supabase.table("childs")
            .update(data)
            .eq("user_id", user_id)
            .eq("name", name)
            .execute()
        )
        return response.data[0]
    except IndexError:
        return []


def delete(user_id: int, name: str) -> dict | list:
    try:
        response = (
            supabase.table("childs")
            .delete()
            .eq("user_id", user_id)
            .eq("name", name)
            .execute()
        )
        return response.data[0]
    except IndexError:
        return []
