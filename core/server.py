from fastapi import FastAPI

app: FastAPI = FastAPI(
    title="Image Processing Service",
    description="Image Processing Service with S3 Bucket Aws",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "title": "Image Processing Service",
        "description": "Image Processing Service with S3 Bucket Aws",
        "version": "1.0.0",
    }
