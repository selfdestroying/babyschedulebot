import json

from models.User import User


def get_users():
    try:
        with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
            user_data = json.load(json_file)
            return user_data
    except FileNotFoundError:
        return {}


def get_user_by_id(id: str) -> User:
    try:
        with open("newjsonfrombot.json", "r", encoding="UTF-8") as json_file:
            user_data = json.load(json_file)
        user = User(**user_data[id])
        print("User already exists")
        return user
    except FileNotFoundError:
        print("File with data doesn't exist. Create empty 'newjsonfrombot.json' file")
        return None
    except KeyError:
        return None


def save_user_data(id, payload: User):
    user_data = get_users()
    with open("newjsonfrombot.json", "w", encoding="UTF-8") as json_file:
        user = payload.model_dump()
        user_data[id] = user
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)
