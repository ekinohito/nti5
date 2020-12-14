from db_base import Session
from models import User, Games


class UserService:
    @staticmethod
    def add_user(username: str, password: str) -> User:
        # with Session as session:
        session = Session()

        username = username.lower()
        user = User(username, password)
        games = Games(user=user)
        session.add(user)

        session.commit()
        session.close()
        return UserService.get_user(username=username)

    @staticmethod
    def get_user(id: int = None, username: str = None) -> User:
        session = Session()

        user: User

        if id:
            user = session.query(User).filter(User.id.is_(id)).first()
        elif username:
            username = username.lower()
            user = session.query(User).filter(User.username.is_(username)).first()

        session.close()
        return user
