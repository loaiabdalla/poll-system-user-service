"""User model definition."""
from datetime import date
from sqlalchemy import Boolean, Column, Date, Integer, String
from app.core.database import Base


class User(Base):
    """SQLAlchemy model for Users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    joining_date = Column(Date, nullable=False, default=date.today)
    is_registered = Column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', is_registered={self.is_registered})>"
