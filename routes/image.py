import time

from fastapi import APIRouter, File, UploadFile, HTTPException, status
import boto3
from config import config
router: APIRouter = APIRouter()

s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_ACCESS_KEY,
    aws_secret_access_key=config.AWS_SECRET_KEY,
    region_name=config.AWS_REGION,
)

@router.get("/")
async def get_all_images(skip: int = 0, limit: int = 100):
    return {"message": "Hello World", "skip": skip, "limit": limit}


@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_name = str(str(time.time()).split(".")[0] + str(file.filename))
        s3.upload_fileobj(
            file.file, config.S3_BUCKET, file_name,
        )
        return {
            "message": "Image uploaded successfully!",
            "file_name": file_name,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error uploading image: {e}"
        )
