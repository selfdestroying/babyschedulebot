from src.api.dbapi.database import supabase


def create(id: int, name: str, phone: str, email: str, problem: str) -> dict | list:
    try:
        response = (
            supabase.table("users")
            .insert(
                {
                    "id": id,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "problem": problem,
                }
            )
            .execute()
        )
        return response.data[0]
    except IndexError:
        return []


def read(id: int) -> dict | list:
    try:
        response = supabase.table("users").select("*").eq("id", id).execute()

        return response.data[0]
    except IndexError:
        return []


def update(
    id: int, name: str = None, phone: str = None, email: str = None
) -> dict | list:
    try:
        data = {}
        if name:
            data["name"] = name
        if phone:
            data["phone"] = phone
        if email:
            data["email"] = email
        response = supabase.table("users").update(data).eq("id", id).execute()
        return response.data[0]
    except IndexError:
        return []


def delete(id: int) -> dict | list:
    try:
        response = supabase.table("users").delete().eq("id", id).execute()
        return response.data[0]
    except IndexError:
        return []
