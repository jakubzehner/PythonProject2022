from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server import auth
from server import schemas
from server.database import crud
from server.database.get_db import get_db

router = APIRouter(prefix='/p_entries', tags=['Planned Entry'], responses={404: {'description': 'Not found'}})


@router.get('/', response_model=list[schemas.planned_entry.PlannedEntrySimplified])
def get_user_planned_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                             current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.planned_entry.get_planned_entries(db, current_user.id, skip, limit)


@router.post('/add', response_model=schemas.planned_entry.PlannedEntry)
def create_planned_entry(planned_entry: schemas.planned_entry.PlannedEntryCreate, db: Session = Depends(get_db),
                         current_user: schemas.user.User = Depends(auth.get_current_user)):
    planned_entry.amount = round(planned_entry.amount, 2)
    planned_entry = crud.planned_entry.create_planned_entry(db, planned_entry, current_user.id)
    return planned_entry


@router.get('/get/{planned_entry_id}', response_model=schemas.planned_entry.PlannedEntry)
def get_entry(planned_entry_id: int, db: Session = Depends(get_db),
              current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.planned_entry.get_planned_entry(db, planned_entry_id, current_user.id)


@router.put('/edit/{planned_entry_id}', response_model=schemas.planned_entry.PlannedEntry)
def edit_entry(planned_entry_id: int, planned_entry: schemas.planned_entry.PlannedEntryCreate,
               db: Session = Depends(get_db),
               current_user: schemas.user.User = Depends(auth.get_current_user)):
    planned_entry.amount = round(planned_entry.amount, 2)
    return crud.planned_entry.update_planned_entry(db, planned_entry_id, current_user.id, planned_entry)


@router.delete('/delete/{planned_entry_id}', response_model=bool)
def delete_entry(planned_entry_id: int, db: Session = Depends(get_db),
                 current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.planned_entry.delete_planned_entry(db, planned_entry_id, current_user.id)
