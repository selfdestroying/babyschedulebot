import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class TimeFilter(BaseFilter):
    async def __call__(self, message: Message):
        is_time_format = re.match(r"^\d{2}:\d{2}$", message.text)
        if is_time_format:
            hours = message.text.split(":")[0]
            minutes = message.text.split(":")[1]
            if (
                int(hours) < 0
                or int(hours) > 23
                or int(minutes) < 0
                or int(minutes) > 59
            ):
                return False
            else:
                return True
        else:
            return False
