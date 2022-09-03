from pydantic import BaseModel
from server.enums import Category
from datetime import date


class EntrySimplified(BaseModel):
    id: int
    category: Category
    name: str | None
    is_outcome: bool
    amount: float

    class Config:
        orm_mode = True


class EntryBase(BaseModel):
    category: Category
    name: str | None = None
    is_outcome: bool
    date: date
    amount: float
    description: str | None = None


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
