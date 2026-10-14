"""User repository for database operations."""
from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    """Repository encapsulating database access for Users."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_registered: Optional[bool] = None,
    ) -> List[User]:
        query = self.db.query(User)
        if is_registered is not None:
            query = query.filter(User.is_registered == is_registered)
        return query.offset(skip).limit(limit).all()

    def create(self, user_in: UserCreate) -> User:
        user_dict = user_in.model_dump()
        if user_dict.get("joining_date") is None:
            user_dict["joining_date"] = date.today()

        user = User(
            first_name=user_dict["first_name"],
            last_name=user_dict["last_name"],
            email=user_dict["email"],
            age=user_dict["age"],
            address=user_dict["address"],
            joining_date=user_dict["joining_date"],
            is_registered=False,  # Explicitly start unregistered
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, db_user: User, update_data: dict) -> User:
        for field, value in update_data.items():
            if hasattr(db_user, field) and value is not None:
                setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def set_registration_status(self, db_user: User, is_registered: bool = True) -> User:
        db_user.is_registered = is_registered
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, db_user: User) -> None:
        self.db.delete(db_user)
        self.db.commit()
