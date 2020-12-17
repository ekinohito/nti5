from sqlalchemy import Column, Integer, String

from db_base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    lol_nickname = Column(String)
    lol_account_id = Column(String)
    steam_id = Column(Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password
