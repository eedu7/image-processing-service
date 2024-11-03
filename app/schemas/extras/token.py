from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description="Access Token")
    refresh_token: str = Field(description="Refresh Token")
    exp: int = Field(description="Expiration Date")
