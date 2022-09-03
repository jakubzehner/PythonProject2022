from sqlalchemy.orm import Session
from server.database.models.planned_entry import PlannedEntry as modelPlannedEntry
from server.schemas.planned_entry import PlannedEntryCreate as schemaPlannedEntryCreate


def get_planned_entry(db: Session, planned_entry_id: int, user_id: int):
    return db.query(modelPlannedEntry).filter(modelPlannedEntry.id == planned_entry_id,
                                              modelPlannedEntry.user_id == user_id).first()


def get_planned_entries(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(modelPlannedEntry).filter(modelPlannedEntry.user_id == user_id).order_by(
        modelPlannedEntry.date.asc(), modelPlannedEntry.id.asc()).offset(skip).limit(limit).all()


def create_planned_entry(db: Session, planned_entry: schemaPlannedEntryCreate, user_id: int):
    db_planned_entry = modelPlannedEntry(**planned_entry.dict(), user_id=user_id)
    db.add(db_planned_entry)
    db.commit()
    db.refresh(db_planned_entry)
    return db_planned_entry


def update_planned_entry(db: Session, planned_entry_id: int, user_id: int, planned_entry: schemaPlannedEntryCreate):
    db_planned_entry = db.query(modelPlannedEntry).filter(modelPlannedEntry.id == planned_entry_id,
                                                          modelPlannedEntry.user_id == user_id).first()

    if db_planned_entry:
        db_planned_entry.amount = planned_entry.amount
        db_planned_entry.is_outcome = planned_entry.is_outcome
        db_planned_entry.name = planned_entry.name
        db_planned_entry.date = planned_entry.date
        db_planned_entry.category = planned_entry.category
        db_planned_entry.description = planned_entry.description
        db_planned_entry.periodicity = planned_entry.periodicity

        db.commit()
        db.refresh(db_planned_entry)

    return db_planned_entry


def delete_planned_entry(db: Session, planned_entry_id: int, user_id: int):
    db_planned_entry = db.query(modelPlannedEntry).filter(modelPlannedEntry.id == planned_entry_id,
                                                          modelPlannedEntry.user_id == user_id).first()

    if db_planned_entry:
        db.delete(db_planned_entry)
        db.commit()
        return True
    return False
