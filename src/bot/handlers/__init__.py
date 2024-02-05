from src.bot.handlers.day import router as day_router
from src.bot.handlers.night import router as night_router
from src.bot.handlers.profile import router as profile_router
from src.bot.handlers.register import router as register_router
from src.bot.handlers.start import router as start_router
from src.bot.handlers.stats import router as stats_router

routers = (
    start_router,
    register_router,
    stats_router,
    profile_router,
    day_router,
    night_router,
)
