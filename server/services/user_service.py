from db_base import Session
from models.user_model import User

class UserService:
    @staticmethod
    def add_user(username: str, password: str) -> User:
        # with Session as session:
        session = Session()

        user = User(username, password)
        session.add(user)

        session.commit()
        session.close()
        return UserService.get_user(username=username)

    @staticmethod
    def get_user(id=None, username=None) -> User:
        session = Session()

        if id:
            user = session.query(User).filter(User.id.is_(id)).first()
        elif username:
            user = session.query(User).filter(User.username.is_(username)).first()

        session.close()
        return user
