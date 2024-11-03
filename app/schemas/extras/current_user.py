from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: Optional[str] = Field(None, description="The user id", examples=[uuid4()])
