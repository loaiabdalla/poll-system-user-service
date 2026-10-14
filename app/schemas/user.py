"""Pydantic schemas for User request and response validation."""
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="User's last name")
    email: EmailStr = Field(..., description="User's unique email address")
    age: int = Field(..., gt=0, lt=150, description="User's age in years")
    address: str = Field(..., min_length=1, max_length=255, description="Physical address")
    joining_date: Optional[date] = Field(default=None, description="Date user joined the company")


class UserCreate(UserBase):
    """Schema for creating a user (is_registered defaults to False)."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating an existing user's information."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0, lt=150)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    joining_date: Optional[date] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    joining_date: date
    is_registered: bool

    model_config = ConfigDict(from_attributes=True)
