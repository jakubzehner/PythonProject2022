from sqlalchemy.orm import Session
from server.database.models.entry import Entry as modelEntry
from server.schemas.entry import EntryCreate as schemaEntryCreate


def get_entries(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(modelEntry).filter(modelEntry.user_id == user_id) \
        .order_by(modelEntry.date.desc(), modelEntry.id.desc()).offset(skip).limit(limit).all()


def get_entry(db: Session, entry_id: int, user_id: int):
    return db.query(modelEntry).filter(modelEntry.id == entry_id, modelEntry.user_id == user_id).first()


def create_entry(db: Session, entry: schemaEntryCreate, user_id: int):
    db_entry = modelEntry(**entry.dict(), user_id=user_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_entry(db: Session, entry_id: int, user_id: int, entry: schemaEntryCreate):
    db_entry = db.query(modelEntry).filter(modelEntry.id == entry_id, modelEntry.user_id == user_id).first()

    if db_entry:
        db_entry.amount = entry.amount
        db_entry.is_outcome = entry.is_outcome
        db_entry.name = entry.name
        db_entry.date = entry.date
        db_entry.category = entry.category
        db_entry.description = entry.description

        db.commit()
        db.refresh(db_entry)

    return db_entry


def delete_entry(db: Session, entry_id: int, user_id: int):
    db_entry = db.query(modelEntry).filter(modelEntry.id == entry_id, modelEntry.user_id == user_id).first()

    if db_entry:
        db.delete(db_entry)
        db.commit()
        return True
    return False
