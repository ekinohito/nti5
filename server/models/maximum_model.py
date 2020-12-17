from sqlalchemy import Column, Integer, String, ForeignKey

from db_base import Base


class Maximum(Base):
    __tablename__ = 'maximum'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False, unique=True)
    value = Column(String(150), nullable=True, unique=True)

    def __repr__(self):
        return f"{self.title}: {self.value}"
