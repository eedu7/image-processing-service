from typing import Dict

from fastapi import APIRouter, Depends, File, UploadFile

from app.crud.image import ImageCRUD
from app.schemas.requests.image import ImageTransformation
from core.exceptions import BadRequestException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user
from core.utils.aws_utils import AWSService
from core.utils.images import create_file_name, crop_image, resize_image, rotate_image

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_images(
    skip: int = 0,
    limit: int = 20,
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
    current_user=Depends(get_current_user),
):
    user_id: str = current_user.id
    return await image_crud.get_all_by("user_id", user_id, skip=skip, limit=limit)


@router.get("/{image_id}")
async def get_image(
    image_id: str,
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
    current_user=Depends(get_current_user),
):
    image = await image_crud.get_by_id(image_id)
    if image.user_id != current_user.id:
        raise BadRequestException("Unauthorized")
    file_name = image.name
    url = await AWSService().generate_presigned_url(file_name)
    return url


@router.post("/upload-image")
async def upload_image(
    image: UploadFile = File(
        ...,
    ),
    current_user=Depends(get_current_user),
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
):
    user_id: str = current_user.id

    file_name = create_file_name(image.filename)

    file_content = await image.read()

    # url = upload_image_to_s3(file_content, file_name, image.content_type)
    url = await AWSService().upload_image_to_s3(
        file_content, file_name, image.content_type
    )
    data = {
        "name": file_name,
        "user_id": user_id,
    }
    new_image = await image_crud.create(data)
    return {
        "id": new_image.id,
        "name": new_image.name,
        "user_id": new_image.user_id,
        "url": url,
    }


@router.post("/transform-image")
async def transform_image(
    image_id: str,
    image_transformation: ImageTransformation,
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
    current_user=Depends(get_current_user),
):
    image_transformation = image_transformation.model_dump()
    saved_image = await image_crud.get_by_id(image_id)
    if saved_image.user_id != current_user.id:
        raise BadRequestException("Unauthorized")

    content_type = saved_image.name.split(".")[-1]

    image = await AWSService().get_image(saved_image.name)

    resize = image_transformation.get("resize", None)
    if resize is not None:
        image = resize_image(image, resize["width"], resize["height"])

    crop: Dict[str, int] | None = image_transformation.get("crop", None)
    if crop is not None:
        image = crop_image(image, crop["x"], crop["y"], crop["width"], crop["height"])

    rotate: int | None = image_transformation.get("rotate", None)
    if rotate is not None:
        image = rotate_image(image, rotate)

    format_image = image_transformation.get("format", None)
    if format_image is not None:
        content_type = format_image
    watermark = image_transformation.get("watermark", None)
    if watermark is not None:
        ...
    filter_image = image_transformation.get("filter", None)
    if filter_image is not None:
        ...

    url = await AWSService().upload_image_to_s3(
        image, saved_image.name, content_type=content_type
    )

    return {"message": "Image successfully transformed", "url": url}


@router.delete("/delete-image/{image_id}")
async def delete_image(
    image_id: str,
    current_user=Depends(get_current_user),
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
):
    image = await image_crud.get_by_id(image_id)
    if image.user_id != current_user.id:
        raise BadRequestException("Unauthorized to delete this image")

    await AWSService().delete_object(image.name)

    await image_crud.delete(image_id)
