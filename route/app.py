from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from utils.middleware import AuthBackend, AuthenticationMiddlewares

from .image import router as image_router
from .user import router as user_router

app: FastAPI = FastAPI(
    title="Image Processing Service",
    description="Image Processing Service",
    version="1.0.0",
)

app.add_middleware(AuthenticationMiddlewares, backend=AuthBackend())


app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(image_router, prefix="/images", tags=["Image"])
