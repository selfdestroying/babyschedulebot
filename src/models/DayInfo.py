from models.Sleep import Sleep
from pydantic import BaseModel


class DayInfo(BaseModel):
    start_night_sleep_time: str
    end_night_sleep_time: str
    night_duration: int
    night_rating: int
    sleeps: list[Sleep]
