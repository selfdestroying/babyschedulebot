from src.api.dbapi import childapi, userapi
from src.utils.differences import calculate_child_age_in_months


def register_user_and_child(data: dict[str, any]):
    id = data.get("user_id")
    user_name = data.get("user_name")
    user_phone = data.get("user_phone")
    user_email = data.get("user_email")
    user_problem = data.get("user_problem")
    child_name = data.get("child_name")
    child_gender = data.get("child_gender")
    child_birth_date = data.get("child_birth_date").strftime("%Y-%m-%d")
    print(child_birth_date)
    food_type = data.get("food_type")
    child_age = calculate_child_age_in_months(child_birth_date)

    userapi.create(
        id=id,
        name=user_name,
        phone=user_phone,
        email=user_email,
        problem=user_problem,
    )
    childapi.create(
        name=child_name,
        gender=child_gender,
        birth_date=child_birth_date,
        age=child_age,
        food_type=food_type,
        user_id=id,
    )