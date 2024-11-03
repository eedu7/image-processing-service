from pydantic import BaseModel


class ResponseUser(BaseModel):
    id: str
    username: str
    email: str
