from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from server import auth
from server import schemas
from server.database import crud
from server.database.get_db import get_db

# Endpoint służący do obsługi wszystkich zapytań związanych z "użytkownikami", umożliwia uzyskanie tokenu, czyli
# "zalogowanie się" użytkownika, obsługuje wszystkie wymagane rodzaje zapytań, tj. zwraca listę użytkowników,
# zwraca szczegóły dotyczące konkretnego użytkownika, umożliwia edycję użytkownika na różne sposoby,
# usuwanie użytkownika

router = APIRouter(prefix='/users', tags=['User'], responses={404: {'description': 'Not found'}})


@router.post('/token', response_model=auth.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/', response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')

    user.password = auth.get_password_hash(user.password)
    return crud.user.create_user(db, user)


@router.get('/', response_model=list[schemas.user.SimpleUserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_users(db, skip, limit)
    return users


@router.get('/me', response_model=schemas.user.User)
def get_current_user(current_user: schemas.user.User = Depends(auth.get_current_user)):
    return current_user


@router.delete('/me', response_model=bool)
def delete_current_user(current_user: schemas.user.User = Depends(auth.get_current_user),
                        db: Session = Depends(get_db)):
    return crud.user.delete_user(db, current_user)


@router.put('/me', response_model=schemas.user.User)
def modify_current_user_personalities(names: schemas.user.UserChangePersonalities,
                                      current_user: schemas.user.User = Depends(auth.get_current_user),
                                      db: Session = Depends(get_db)):
    current_user.first_name = names.first_name
    current_user.last_name = names.last_name
    return crud.user.update_user_personalities(db, current_user)


@router.patch('/me/{balance_change}', response_model=schemas.user.User)
def change_current_user_balance(balance_change: float, current_user: schemas.user.User = Depends(auth.get_current_user),
                                db: Session = Depends(get_db)):
    current_user.balance += balance_change
    current_user.balance = round(current_user.balance, 2)
    return crud.user.update_user_balance(db, current_user)


@router.put('/me/{new_balance}', response_model=schemas.user.User)
def set_current_user_balance(new_balance: float, current_user: schemas.user.User = Depends(auth.get_current_user),
                             db: Session = Depends(get_db)):
    current_user.balance = new_balance
    current_user.balance = round(current_user.balance, 2)
    return crud.user.update_user_balance(db, current_user)


@router.put('/me_password', response_model=schemas.user.User)
def change_current_user_password(passwords: schemas.user.UserChangePassword,
                                 current_user: schemas.user.User = Depends(auth.get_current_user),
                                 db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, current_user.username, passwords.old_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect old password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    if passwords.old_password == passwords.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password can't be the same as old password",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user.password = auth.get_password_hash(passwords.new_password)
    return crud.user.update_user_password(db, user)
