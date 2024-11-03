from typing import Optional

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: Optional[str] = Field(None, description="The user id")
