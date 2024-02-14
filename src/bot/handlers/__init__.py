from src.bot.handlers.day import day_router
from src.bot.handlers.menu import menu_router
from src.bot.handlers.night import night_router
from src.bot.handlers.register import register_router
from src.bot.handlers.start import start_router

routers = (start_router, register_router, menu_router, day_router, night_router)
