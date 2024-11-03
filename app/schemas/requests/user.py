from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "<PASSWORD>",
                "email": "<EMAIL>",
            }
        }
