from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import UserCrud
from db import get_async_session
from model import User
from schema.token import Token
from schema.user import LoginUser, RegisterUser, UserRead
from utils.dependency.authentication import AuthenticationRequired

router = APIRouter()


@router.get(
    "/", response_model=List[UserRead], dependencies=[Depends(AuthenticationRequired)]
)
async def get_users(
    skip: int = 0, limit: int = 20, session: AsyncSession = Depends(get_async_session)
) -> List[User]:
    crud = UserCrud(session=session)
    users = await crud.get_all(skip=skip, limit=limit)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return users


@router.post("/", response_model=UserRead)
async def register(
    data: RegisterUser, session: AsyncSession = Depends(get_async_session)
):
    crud = UserCrud(session=session)
    user = await crud.register_user(data.model_dump())
    if user:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED, detail="User created successfully"
        )


@router.post("/login", response_model=Token)
async def login(
    data: LoginUser, session: AsyncSession = Depends(get_async_session)
) -> Token:
    crud = UserCrud(session=session)
    return await crud.login_user(email=data.email, password=data.password)
