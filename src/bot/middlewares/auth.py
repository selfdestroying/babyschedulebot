from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

import pytz
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.analysis import ideal_data
from src.api.dbapi import childapi, scheduleapi, userapi


class AuthMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        message: Message = event
        user = message.from_user
        state: FSMContext = data.get("state")
        res = await state.get_data()
        if res:
            print("User already registered")
        else:
            current_date = datetime.now(pytz.timezone("Etc/GMT-3"))
            dbuser = userapi.read(user.id)
            dbchild = childapi.read(user.id)
            dbschedule = scheduleapi.read(user.id, current_date)
            dbdata = dbuser
            dbdata.update(dbchild)
            dbdata.update(dbschedule)
            dbdata.update({"ideal_data_for_age": ideal_data.ideal_data[dbchild["age"]]})
            if dbuser:
                await state.update_data(dbdata)
            else:
                print("User not registered")

        return await handler(event, data)
