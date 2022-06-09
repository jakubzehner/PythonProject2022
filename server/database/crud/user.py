from sqlalchemy.orm import Session
from server.database.models.user import User as modelUser
from server.schemas.user import UserCreate as schemaUserCreate
from server.schemas.user import User as schemaUser


# Operacje na bazie danych dotyczące "użytkowników"

def get_user(db: Session, user_id: int):
    return db.query(modelUser).filter(modelUser.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(modelUser).filter(modelUser.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modelUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemaUserCreate):
    db_user = modelUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_personalities(db: Session, user: schemaUser):
    db_user = db.query(modelUser).filter(modelUser.id == user.id).first()
    if db_user:
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db.commit()
        db.refresh(db_user)
    return db_user


def update_user_balance(db: Session, user: schemaUser):
    db_user = db.query(modelUser).filter(modelUser.id == user.id).first()
    if db_user:
        db_user.balance = user.balance
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user: schemaUser):
    db_user = db.query(modelUser).filter(modelUser.id == user.id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def update_user_password(db: Session, user: schemaUserCreate):
    db_user = db.query(modelUser).filter(modelUser.username == user.username).first()
    if db_user:
        db_user.password = user.password
        db.commit()
        db.refresh(db_user)
    return db_user
