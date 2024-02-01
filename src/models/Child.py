from pydantic import BaseModel


class Child(BaseModel):
    name: str
    gender: str
    birth_date: str
    age: str
    food_type: str
