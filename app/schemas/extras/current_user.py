from typing import Optional

from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: Optional[str] = None
