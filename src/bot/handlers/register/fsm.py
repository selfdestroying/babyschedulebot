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