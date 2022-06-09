from pydantic import BaseModel


# Modele pydatnic dotyczące "użytkowników", umożliwiają łatwe zarządzanie danymi, walidacje danych, a także
# automatyczne generowanie wymaganego body w formacie json do zapytań, oraz odpowiedzi z serwera również w formacie json

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserChangePersonalities(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class SimpleUserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    balance: float

    class Config:
        orm_mode = True
