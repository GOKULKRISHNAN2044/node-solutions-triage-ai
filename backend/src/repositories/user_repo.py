from sqlalchemy.orm import Session
from repositories.schema.schema import User
from utils.security import hash_password, verify_password


class UserRepository:
    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username.strip().lower()).first()

    def create_user(self, db: Session, username: str, password: str) -> User:
        user = User(
            username=username.strip().lower(),
            password_hash=hash_password(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def verify_credentials(self, db: Session, username: str, password: str) -> User | None:
        user = self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(user.password_hash, password):
            return None
        return user

    def seed_default_admin(self, db: Session) -> None:
        """
        Seeds default admin user if no users exist in the database.
        Default login:
          Username: admin
          Password: nodeadmin123
        """
        if db.query(User).count() == 0:
            self.create_user(db, "admin", "nodeadmin123")
