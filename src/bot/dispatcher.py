"""This file contains build dispatcher logic."""

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from src.bot.handlers import routers


def get_dispatcher(
    storage: BaseStorage = MemoryStorage(),
    fsm_strategy: FSMStrategy | None = FSMStrategy.USER_IN_CHAT,
    event_isolation: BaseEventIsolation | None = None,
):
    """This function set up dispatcher with routers, filters and middlewares."""
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation,
    )
    for router in routers:
        dp.include_router(router)

    # Register middlewares

    return dp
