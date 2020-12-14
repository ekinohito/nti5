from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

import models

from db_base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    games = relationship('models.Games', back_populates="parent", uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
