from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server import auth
from server import schemas
from server.database import crud
from server.database.get_db import get_db

from .user import change_current_user_balance

router = APIRouter(prefix='/entries', tags=['Entry'], responses={404: {'description': 'Not found'}})


@router.get('/', response_model=list[schemas.entry.EntrySimplified])
def get_user_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.entry.get_entries(db, current_user.id, skip, limit)


@router.post('/add', response_model=schemas.entry.Entry)
def create_entry(entry: schemas.entry.EntryCreate, db: Session = Depends(get_db),
                 current_user: schemas.user.User = Depends(auth.get_current_user)):
    entry.amount = round(entry.amount, 2)
    entry = crud.entry.create_entry(db, entry, current_user.id)
    change = entry.amount
    if entry.is_outcome:
        change = -change

    change_current_user_balance(change, current_user, db)
    return entry


@router.get('/get/{entry_id}', response_model=schemas.entry.Entry)
def get_entry(entry_id: int, db: Session = Depends(get_db),
              current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.entry.get_entry(db, entry_id, current_user.id)


@router.put('/edit/{entry_id}', response_model=schemas.entry.Entry)
def edit_entry(entry_id: int, entry: schemas.entry.EntryCreate, db: Session = Depends(get_db),
               current_user: schemas.user.User = Depends(auth.get_current_user)):
    entry.amount = round(entry.amount, 2)

    entry_db = crud.entry.get_entry(db, entry_id, current_user.id)
    change = entry_db.amount
    if not entry_db.is_outcome:
        change = -change
    if entry.is_outcome:
        change -= entry.amount
    else:
        change += entry.amount

    change_current_user_balance(change, current_user, db)

    return crud.entry.update_entry(db, entry_id, current_user.id, entry)


@router.delete('/delete/{entry_id}', response_model=bool)
def delete_entry(entry_id: int, db: Session = Depends(get_db),
                 current_user: schemas.user.User = Depends(auth.get_current_user)):
    entry_db = crud.entry.get_entry(db, entry_id, current_user.id)
    change = entry_db.amount
    if not entry_db.is_outcome:
        change = -change
    change_current_user_balance(change, current_user, db)

    return crud.entry.delete_entry(db, entry_id, current_user.id)
