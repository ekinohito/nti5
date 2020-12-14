from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import models

from db_base import Base


class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    lol_nickname = Column(String)
    lol_account_id = Column(Integer)

    user = relationship('models.User', back_populates="child", uselist=False)
