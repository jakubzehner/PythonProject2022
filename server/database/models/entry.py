from datetime import date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, Enum
from sqlalchemy.orm import relationship

from server.database.database import Base
from server.enums import Category


# klasa służąca do opisu tabeli w bazie danych, ponieważ projekt wykorzystuje ORM, konretnie sqlalchemy

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    category = Column(Enum(Category), nullable=False)
    name = Column(String)
    is_outcome = Column(Boolean, nullable=False, default=True)
    date = Column(Date, nullable=False, default=date.today())
    amount = Column(Float, nullable=False)
    description = Column(String)

    user = relationship('User', back_populates='entries')
