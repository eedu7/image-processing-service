from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from utils.middleware import AuthenticationMiddlewares, AuthBackend
from .user import router as user_router
app: FastAPI = FastAPI(
    title="Image Processing Service",
    description="Image Processing Service",
    version="1.0.0",
)

app.add_middleware(AuthenticationMiddlewares, backend=AuthBackend())


app.include_router(user_router, prefix="/user", tags=["User"])
