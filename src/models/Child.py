from pydantic import BaseModel


class Child(BaseModel):
    name: str
    gender: str
    age: str
    food_type: str
