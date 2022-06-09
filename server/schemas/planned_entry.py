from pydantic import BaseModel
from server.enums import Category, Period
from datetime import date


# Modele pydatnic dotyczące "planowanych wpisów", umożliwiają łatwe zarządzanie danymi, walidacje danych, a także
# automatyczne generowanie wymaganego body w formacie json do zapytań, oraz odpowiedzi z serwera również w formacie json


class PlannedEntryBase(BaseModel):
    category: Category
    name: str | None = None
    is_outcome: bool
    date: date
    amount: float
    description: str | None = None
    periodicity: Period


class PlannedEntrySimplified(BaseModel):
    id: int
    category: Category
    name: str | None
    is_outcome: bool
    amount: float
    periodicity: Period

    class Config:
        orm_mode = True


class PlannedEntryCreate(PlannedEntryBase):
    pass


class PlannedEntry(PlannedEntryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
