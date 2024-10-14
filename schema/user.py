from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com", "<EMAIL>"])


class RegisterUser(UserBase):
    name: str = Field(..., min_length=3, max_length=50, examples=["John Doe"])
    password: str = Field(..., min_length=8, max_length=30, examples=["password123"])


class LoginUser(UserBase):
    password: str = Field(..., min_length=8, max_length=30, examples=["password123"])


class UserRead(UserBase):
    id: int = Field(..., examples=[1, 2])
    name: str = Field(..., min_length=3, max_length=50, examples=["John Doe"])
    is_active: bool = Field(..., examples=[True, False])


class UserProfileData(UserRead):
    is_staff: bool = Field(..., examples=[True, False])
    is_admin: bool = Field(..., examples=[True, False])
    is_superuser: bool = Field(..., examples=[True, False])
    created_at: datetime = Field(..., examples=[datetime.now(), datetime.now()])
    updated_at: datetime = Field(..., examples=[datetime.now(), datetime.now()])


class CurrentUser(BaseModel):
    id: int | None = Field(None, description="ID of the user",examples=[1, 2])