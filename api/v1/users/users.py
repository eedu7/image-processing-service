from fastapi import APIRouter, Depends

from app.crud.user import UserCRUD
from app.schemas.requests.user import LoginUser, RegisterUser
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

router: APIRouter = APIRouter()


@router.get("/", dependencies=[Depends(AuthenticationRequired)])
async def get_all_users(
    skip: int = 0, limit: int = 20, user_crud: UserCRUD = Depends(Factory.get_user_crud)
):
    return await user_crud.get_all(skip=skip, limit=limit)


@router.post("/")
async def register_user(
    user_data: RegisterUser, user_crud: UserCRUD = Depends(Factory.get_user_crud)
):
    return await user_crud.register_user(user_data.model_dump())


@router.post("/login")
async def login_user(
    user_data: LoginUser, user_crud: UserCRUD = Depends(Factory.get_user_crud)
):
    return await user_crud.login_user(user_data.model_dump())


@router.get("/me", dependencies=[Depends(AuthenticationRequired)])
async def get_current_user(user=Depends(get_current_user)):
    return user
