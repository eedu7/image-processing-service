from fastapi import APIRouter, Depends, status

from app.crud.user import UserCRUD
from app.schemas.extras import Token
from app.schemas.requests.user import LoginUser, RegisterUser
from app.schemas.responses.user import ResponseUser
from core.exceptions import BadRequestException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user

router: APIRouter = APIRouter()


@router.post("/", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: RegisterUser, user_crud: UserCRUD = Depends(Factory.get_user_crud)
):
    """
    Register a new user.

    This endpoint creates a new user in the system with the provided registration data.

    - **user_data**: The registration details of the user.

    Returns the newly created user data.
    """
    return await user_crud.register_user(user_data.model_dump())


@router.post("/login", response_model=Token)
async def login_user(
    user_data: LoginUser, user_crud: UserCRUD = Depends(Factory.get_user_crud)
):
    """
    Log in a user.

    This endpoint authenticates a user with the provided login credentials.

    - **user_data**: The login credentials (username and password).

    Returns the authenticated user's data.
    """
    return await user_crud.login_user(user_data.model_dump())


@router.get(
    "/me", dependencies=[Depends(AuthenticationRequired)], response_model=ResponseUser
)
async def get_current_user(user=Depends(get_current_user)):
    """
    Retrieve current user information.

    This endpoint returns the profile data of the currently authenticated user.

    Requires authentication.
    """
    return user


@router.delete(
    "/",
    dependencies=[Depends(AuthenticationRequired)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: str,
    user_crud: UserCRUD = Depends(Factory.get_user_crud),
    current_user=Depends(get_current_user),
):
    """
    Delete a user.

    This endpoint deletes the specified user account if the user ID matches the currently authenticated user.

    - **user_id**: ID of the user to delete.

    Raises a `400 Bad Request` if the user ID does not match the current user.
    """
    if user_id != current_user.id:
        raise BadRequestException("Unauthorized")

    await user_crud.delete(user_id)
