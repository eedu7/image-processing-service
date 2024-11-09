from fastapi import APIRouter, Depends, File, UploadFile

from app.crud.image import ImageCRUD
from app.schemas.requests.image import ImageTransformation
from core.exceptions import BadRequestException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user
from core.utils.aws_utils import AWSService
from core.utils.images import apply_image_transformations, create_file_name

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
    """
    Transform an image by applying resizing, cropping, rotating, watermarking, filtering, and/or format change.
    If no format is specified, the original format is preserved.

    Args:
        image_id (str): ID of the image to transform.
        image_transformation (ImageTransformation): The transformations to apply.
        image_crud (ImageCRUD): Dependency for interacting with the image database.
        current_user: The authenticated user making the request.

    Returns:
        dict: A dictionary containing a success message and the URL of the transformed image.

    Raises:
        BadRequestException: If the user is unauthorized or a transformation fails.
    """
    transformations = image_transformation.model_dump()
    saved_image = await image_crud.get_by_id(image_id)

    if saved_image.user_id != current_user.id:
        raise BadRequestException("Unauthorized")

    # Retrieve image bytes from AWS S3
    image_bytes = await AWSService().get_image(saved_image.name)

    # Determine the original format
    original_format = saved_image.name.rsplit(".", 1)[-1].lower()

    # Apply all transformations using the helper function
    try:
        image_bytes = apply_image_transformations(
            image_bytes, transformations, original_format
        )
    except ValueError as e:
        raise BadRequestException(str(e))

    # Determine content type and file name for the transformed image
    format_image = transformations.get("format", original_format).lower()
    content_type = f"image/{format_image}"
    new_file_name = (
        saved_image.name.rsplit(".", 1)[0] + f".{format_image}"
        if format_image != original_format
        else saved_image.name
    )

    # Upload the transformed image back to S3
    url = await AWSService().upload_image_to_s3(
        image_bytes, new_file_name, content_type=content_type
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
