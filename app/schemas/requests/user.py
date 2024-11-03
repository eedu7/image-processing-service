from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: str
    password: str
