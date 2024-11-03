from fastapi import APIRouter, Depends

from app.crud.user import UserCRUD
from app.schemas.requests.user import RegisterUser
from core.factory.factory import Factory

router: APIRouter = APIRouter()


@router.post("/")
async def register_user(user_data: RegisterUser, user_crud: UserCRUD = Depends(Factory.get_user_crud)):
    return await user_crud.register_user(user_data.model_dump())
