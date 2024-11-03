from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        description="The email address of the user",
        examples=["john.doe@example.com"],
    )
    password: str = Field(
        ..., description="The password of the user", examples=["password123"]
    )


class RegisterUser(UserBase):
    username: str = Field(
        ..., description="The username of the user", examples=["John Doe"]
    )


class LoginUser(UserBase):
    pass
