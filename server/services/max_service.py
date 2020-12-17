from db_base import Session
from models import Maximum


class MaxService:
    @staticmethod
    def add_max(title: str, value: str) -> Maximum:
        # with Session as session:
        session = Session()

        maximum = Maximum(title, value)

        session.add(maximum)

        session.commit()
        session.close()
        return Maximum.get_max(title=title)

    @staticmethod
    def get_max(id: int = None, title: str = None) -> Maximum:
        session = Session()

        maximum: Maximum = None

        if id:
            maximum = session.query(Maximum).filter(Maximum.id.is_(id)).first()
        elif title:
            maximum = session.query(Maximum).filter(Maximum.title.is_(title)).first()

        session.close()
        return maximum

    @staticmethod
    def update_maximum(value: str, id: int = None, title: str = None, ) -> Maximum:
        session = Session()

        maximum: Maximum = None

        if id:
            maximum = session.query(Maximum).filter(Maximum.id.is_(id)).first()
        elif title:
            maximum = session.query(Maximum).filter(Maximum.title.is_(title)).first()

        if maximum:
            maximum.value = value
            session.commit()
        session.close()