from datetime import date

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Enum
from sqlalchemy.orm import relationship

from server.database.database import Base
from server.enums import Color, Icon


class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    actual_amount = Column(Float, nullable=False, default=0.0)
    date = Column(Date, nullable=False, default=date.today())
    color = Column(Enum(Color), nullable=False)
    icon = Column(Enum(Icon), nullable=False)
    description = Column(String)

    user = relationship('User', back_populates='goals')
