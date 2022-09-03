from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from server.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    balance = Column(Float, nullable=False, default=0.0)

    entries = relationship('Entry', back_populates='user')
    planned_entries = relationship('PlannedEntry', back_populates='user')
    goals = relationship('Goal', back_populates='user')
