# backend/app/schemas.py
from pydantic import BaseModel

class PersonBase(BaseModel):
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True

# Use the same class for response, no need for complex models
Person = PersonBase