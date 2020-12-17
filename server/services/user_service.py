from db_base import Session
from models import User


class UserService:
    @staticmethod
    def add_user(username: str, password: str) -> User:
        # with Session as session:
        session = Session()

        username = username.lower()
        user = User(username, password)
        session.add(user)

        session.commit()
        session.close()
        return UserService.get_user(username=username)

    @staticmethod
    def get_user(id: int = None, username: str = None) -> User:
        session = Session()

        user: User = None

        if id:
            user = session.query(User).filter(User.id.is_(id)).first()
        elif username:
            username = username.lower()
            user = session.query(User).filter(User.username.is_(username)).first()

        session.close()
        return user

    @staticmethod
    def update_games(user_id: int, **kwargs) -> User:
        session = Session()
        user = session.query(User).filter(User.id.is_(user_id)).first()
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
        session.close()
        return user
