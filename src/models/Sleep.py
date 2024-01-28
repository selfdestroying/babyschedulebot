from pydantic import BaseModel


class Sleep(BaseModel):
    start_sleep_time: str
    end_sleep_time: str
    sleep_duration: int
