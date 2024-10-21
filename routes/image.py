import time

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
import boto3
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from crud.image import ImageCrud
from db import get_async_session

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
async def upload_image(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    try:
        image_crud: ImageCrud = ImageCrud(session)
        file_name = str(str(time.time()).split(".")[0] + str(file.filename))
        s3.upload_fileobj(
            file.file, config.S3_BUCKET, file_name,
        )
        await image_crud.create({
            "name": file_name,
        })
        file_url: str = f"https://{config.S3_BUCKET}.s3.{config.AWS_REGION}.amazonaws.com/{file_name}"
        return {
            "message": "Image uploaded successfully!",
            "file_url": file_url,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error uploading image: {e}"
        )

