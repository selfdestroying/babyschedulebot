from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

menu_router = Router(name="menu")


class MenuGroup(StatesGroup):
    menu = State()
