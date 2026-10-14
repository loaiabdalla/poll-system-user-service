"""User Controller - REST API routes for User resource."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (Unregistered by default)",
)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """
    Creates a new user. The newly created user will have `is_registered = False`.
    Registration is a separate step via the `/register` endpoint.
    """
    return service.create_user(user_in)


@router.get(
    "",
    response_model=List[UserResponse],
    summary="List all users",
)
def list_users(
    skip: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(100, ge=1, le=500, description="Page limit"),
    is_registered: Optional[bool] = Query(None, description="Filter by registered status"),
    service: UserService = Depends(get_user_service),
):
    """Retrieve users with pagination and optional registration status filter."""
    return service.list_users(skip=skip, limit=limit, is_registered=is_registered)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """Get details for a specific user by ID."""
    return service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user details",
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    """Update fields for an existing user."""
    return service.update_user(user_id, user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user (cascades answers in Poll Service)",
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """
    Delete a user from the system.
    Automatically triggers a cascading delete of all poll answers submitted by this user in the Poll Service.
    """
    await service.delete_user(user_id)
    return None


@router.patch(
    "/{user_id}/register",
    response_model=UserResponse,
    summary="Register user (Dedicated registration endpoint)",
)
@router.post(
    "/{user_id}/register",
    response_model=UserResponse,
    summary="Register user (Dedicated registration endpoint - POST alias)",
)
def register_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """
    Dedicated endpoint to register an existing user.
    Switches `is_registered` to `True`. Only registered users can answer poll questions.
    """
    return service.register_user(user_id)
