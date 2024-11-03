from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


class ResponseUser(BaseModel):
    id: str = Field(..., description="The user id", examples=[uuid4()])
    username: str = Field(..., description="The user username", examples=["John Doe"])
    email: EmailStr = Field(
        ..., description="The user email", examples=["john.doe@example.com"]
    )
