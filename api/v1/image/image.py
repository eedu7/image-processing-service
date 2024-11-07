from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse

from app.crud.image import ImageCRUD
from app.schemas.requests.image import ImageTransformation
from core.exceptions import BadRequestException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user
from core.utils import remove_image
from core.utils.aws_utils import upload_image_to_s3
from core.utils.images import create_file_name

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
    media_type = file_name.split(".")[-1]
    file_path: str = f"images/{file_name}"
    return FileResponse(file_path, media_type=f"image/{media_type}")


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

    url = upload_image_to_s3(file_content, file_name, image.content_type)

    data = {
        "name": file_name,
        "user_id": user_id,
    }
    await image_crud.create(data)
    data["url"] = url
    return data


@router.post("/transform-image")
async def transform_image(
    image_id: str,
    image_transformation: ImageTransformation,
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
    current_user=Depends(get_current_user),
):
    return image_transformation.model_dump(exclude_none=True)


@router.delete("/delete-image/{image_id}")
async def delete_image(
    image_id: str,
    current_user=Depends(get_current_user),
    image_crud: ImageCRUD = Depends(Factory.get_image_crud),
):
    image = await image_crud.get_by_id(image_id)
    if image.user_id != current_user.id:
        raise BadRequestException("Unauthorized to delete this image")

    remove_image(image.name)
    await image_crud.delete(image_id)
