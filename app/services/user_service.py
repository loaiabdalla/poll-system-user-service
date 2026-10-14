"""User business logic service layer."""
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.poll_client import PollClient


class UserService:
    """Service layer coordinating user business logic and external integrations."""

    def __init__(self, db: Session, poll_client: Optional[PollClient] = None):
        self.repository = UserRepository(db)
        self.poll_client = poll_client or PollClient()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
        return user

    def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
        is_registered: Optional[bool] = None,
    ) -> List[User]:
        return self.repository.get_all(skip=skip, limit=limit, is_registered=is_registered)

    def create_user(self, user_in: UserCreate) -> User:
        existing = self.repository.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A user with email '{user_in.email}' already exists."
            )
        return self.repository.create(user_in)

    def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)
        update_data = user_in.model_dump(exclude_unset=True)

        # Check if email is being changed and if it is already taken
        if "email" in update_data and update_data["email"] != user.email:
            existing = self.repository.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{update_data['email']}' is already in use by another user."
                )

        return self.repository.update(user, update_data)

    def register_user(self, user_id: int) -> User:
        """
        Switch user's is_registered status to True.
        Creating a user and registering a user are two separate steps.
        """
        user = self.get_user_by_id(user_id)
        if user.is_registered:
            return user  # Already registered, idempotent
        return self.repository.set_registration_status(user, is_registered=True)

    async def delete_user(self, user_id: int) -> None:
        """
        Deletes the user and cascades deletion of all answers submitted by this user in Poll Service.
        """
        user = self.get_user_by_id(user_id)
        # Notify Poll Service to cascade-delete all answers submitted by this user
        await self.poll_client.delete_user_answers(user_id)
        # Delete user from local database
        self.repository.delete(user)
