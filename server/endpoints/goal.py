from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server import auth
from server import schemas
from server.database import crud
from server.database.get_db import get_db

router = APIRouter(prefix='/goals', tags=['Goal'], responses={404: {'description': 'Not found'}})


@router.get('/', response_model=list[schemas.goal.GoalSimplified])
def get_user_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                   current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.goal.get_goals(db, current_user.id, skip, limit)


@router.post('/add', response_model=schemas.goal.Goal)
def create_goal(goal: schemas.goal.GoalCreate, db: Session = Depends(get_db),
                current_user: schemas.user.User = Depends(auth.get_current_user)):
    goal.actual_amount = round(goal.actual_amount, 2)
    goal.target_amount = round(goal.target_amount, 2)
    goal = crud.goal.create_goal(db, goal, current_user.id)
    return goal


@router.get('/get/{goal_id}', response_model=schemas.goal.Goal)
def get_goal(goal_id: int, db: Session = Depends(get_db),
             current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.goal.get_goal(db, goal_id, current_user.id)


@router.put('/edit/{goal_id}', response_model=schemas.goal.Goal)
def edit_goal(goal_id: int, goal: schemas.goal.GoalCreate, db: Session = Depends(get_db),
              current_user: schemas.user.User = Depends(auth.get_current_user)):
    goal.actual_amount = round(goal.actual_amount, 2)
    goal.target_amount = round(goal.target_amount, 2)
    return crud.goal.update_goal(db, goal_id, current_user.id, goal)


@router.delete('/delete/{goal_id}', response_model=bool)
def delete_goal(goal_id: int, db: Session = Depends(get_db),
                current_user: schemas.user.User = Depends(auth.get_current_user)):
    return crud.goal.delete_goal(db, goal_id, current_user.id)
