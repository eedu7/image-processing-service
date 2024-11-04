from fastapi import APIRouter
from .image import router


image_router: APIRouter = APIRouter()
image_router.include_router(router, tags=["Image"])

__all__ = ["image_router"]
