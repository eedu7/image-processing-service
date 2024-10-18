import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from schema.image import TransformationModel
from utils.image_service import transform_image

router = APIRouter()

UPLOAD_DIRECTORY = Path("images")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.post(
    "/upload-image/",
    summary="Upload an image",
    description="Allows JPEG, JPG, or PNG image upload.",
)
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads an image to the server.

    - **file**: The image file to be uploaded.

    Returns:
    - **filename**: The name of the uploaded file.
    - **message**: A success message.
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Only JPEG, JPG, and PNG are supported.",
        )

    file_location = UPLOAD_DIRECTORY / file.filename
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(
        content={"filename": file.filename, "message": "Image uploaded successfully!"}
    )


@router.post(
    "/{image_id}/transform",
    summary="Transform an uploaded image",
    description="Resize, crop, rotate, apply filters, or change format of an image.",
)
async def image_transform(image_id: str, transformation_data: TransformationModel):
    """
    Applies transformations (resize, crop, rotate, filters, and format change) to an image.

    - **image_id**: The ID or name of the image to transform.
    - **transformation_data**: Contains the transformations to apply (resize, crop, rotate, filter, format).

    Returns:
    - **message**: Transformation status message.
    """
    file_path = UPLOAD_DIRECTORY / f"{image_id}.png"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found.")

    try:
        output_file_path = transform_image(file_path, transformation_data)
        return JSONResponse(
            content={
                "message": "Image transformed successfully!",
                "output": str(output_file_path),
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error during image transformation: {e}"
        )
