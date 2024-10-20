from fastapi import FastAPI

from .image import router as image_router

app: FastAPI = FastAPI(
    title="Image Processing Service",
    description="Image Processing Service",
    version="1.0.0",
)


app.include_router(image_router, prefix="/image", tags=["Image"])
