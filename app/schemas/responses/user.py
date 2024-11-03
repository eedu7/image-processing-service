from pydantic import UUID4, BaseModel, EmailStr, Field


class ResponseUser(BaseModel):
    id: str | UUID4 = Field(..., description="The user id")
    username: str = Field(..., description="The user username", examples=["John Doe"])
    email: EmailStr = Field(
        ..., description="The user email", examples=["john.doe@example.com"]
    )
