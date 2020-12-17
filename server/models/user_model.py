from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db_base import Base

class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    lol_nickname = Column(String)
    lol_account_id = Column(String)

    steam_id = Column(Integer)

    user = relationship('User', back_populates="games", uselist=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    lol_nickname = Column(String)
    lol_account_id = Column(String)
    steam_id = Column(String)
    fortnite_id = Column(String)
    games = relationship(Games, back_populates="user", uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
