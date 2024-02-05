from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.api.dbapi import userapi


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message):
        id = message.from_user.id
        user = userapi.read(id)
        if user:
            return False
        else:
            return True
