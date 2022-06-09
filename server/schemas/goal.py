from pydantic import BaseModel
from server.enums import Color, Icon
from datetime import date

# Modele pydatnic dotyczące "celów", umożliwiają łatwe zarządzanie danymi, walidacje danych, a także automatyczne
# generowanie wymaganego body w formacie json do zapytań, oraz odpowiedzi z serwera również w formacie json


class GoalBase(BaseModel):
    name: str
    target_amount: float
    actual_amount: float
    date: date
    color: Color
    icon: Icon
    description: str | None = None


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class GoalSimplified(BaseModel):
    id: int
    name: str
    target_amount: float
    actual_amount: float
    color: Color
    icon: Icon

    class Config:
        orm_mode = True
