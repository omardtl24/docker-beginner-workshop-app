# backend/app/schemas.py
from pydantic import BaseModel

class PersonBase(BaseModel):
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True

Person = PersonBase