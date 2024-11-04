from fastapi import APIRouter

from .users import users_router
from .image import image_router

v1_router = APIRouter()
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(image_router, prefix="/image")
