from fastapi import Depends, Request

from app.crud.user import UserCRUD
from core.factory import Factory


async def get_current_user(
    request: Request, user_crud: UserCRUD = Depends(Factory.get_user_crud)
):
    user = await user_crud.get_by_id(request.user.id)
    return user
