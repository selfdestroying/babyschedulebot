from aiogram.fsm.state import State, StatesGroup


class RegisterGroup(StatesGroup):
    confirmation = State()
    user_phone = State()
    user_email = State()
    user_problem = State()
    child_name = State()
    child_gender = State()
    child_birth_date = State()
    food_type = State()
    start_night_time = State()
    end_night_time = State()
    night_wake_up_count = State()
    night_rating = State()
