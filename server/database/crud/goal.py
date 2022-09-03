from sqlalchemy.orm import Session
from server.database.models.goal import Goal as modelGoal
from server.schemas.goal import GoalCreate as schemaGoalCreate


def create_goal(db: Session, goal: schemaGoalCreate, user_id: int):
    db_goal = modelGoal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def get_goal(db: Session, goal_id: int, user_id: int):
    return db.query(modelGoal).filter(modelGoal.id == goal_id, modelGoal.user_id == user_id).first()


def delete_goal(db: Session, goal_id: int, user_id: int):
    db_goal = db.query(modelGoal).filter(modelGoal.id == goal_id, modelGoal.user_id == user_id).first()

    if db_goal:
        db.delete(db_goal)
        db.commit()
        return True
    return False


def get_goals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(modelGoal).filter(modelGoal.user_id == user_id).offset(skip).limit(limit).all()


def update_goal(db: Session, goal_id: int, user_id: int, goal: schemaGoalCreate):
    db_goal = db.query(modelGoal).filter(modelGoal.id == goal_id, modelGoal.user_id == user_id).first()

    if db_goal:
        db_goal.name = goal.name
        db_goal.date = goal.date
        db_goal.description = goal.description
        db_goal.target_amount = goal.target_amount
        db_goal.actual_amount = goal.actual_amount
        db_goal.color = goal.color
        db_goal.icon = goal.icon

        db.commit()
        db.refresh(db_goal)

    return db_goal
