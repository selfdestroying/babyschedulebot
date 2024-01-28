from pydantic import BaseModel

from models.Child import Child
from models.DayInfo import DayInfo


class User(BaseModel):
    name: str
    phone: str
    email: str
    child: Child
    schedule: dict[str, DayInfo]
