from fastapi import FastAPI

from api.v1.users.users import router

app: FastAPI = FastAPI(
    title="Image Processing Service",
    description="Image Processing Service with S3 Bucket Aws",
    version="1.0.0",
)


app.include_router(router, prefix="/user", tags=["User"])


@app.get("/")
async def root():
    return {
        "title": "Image Processing Service",
        "description": "Image Processing Service with S3 Bucket Aws",
        "version": "1.0.0",
    }
