import shutil
from pathlib import Path
from typing import Dict

from PIL import Image
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from schema.image import TransformationModel

router: APIRouter = APIRouter()

UPLOAD_DIRECTORY = Path("images")

UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Only JPEG and PNG are supported.",
        )

    file_location = UPLOAD_DIRECTORY / file.filename

    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(
        content={"filename": file.filename, "message": "Image uploaded successfully!"}
    )


@router.post("/{image_id}/transform")
async def image_transform(image_id: str, transformation_data: TransformationModel):
    file_path = UPLOAD_DIRECTORY / "image_1.png"
    print(file_path)
    try:
        transformation_data = transformation_data.model_dump()
        resize_image = transformation_data.get("resize", None)
        crop_image = transformation_data.get("crop", None)
        rotate_image: float | None = transformation_data.get("rotate", None)
        format_image: str | None = transformation_data.get("format", None)
        filter_image: Dict[str, bool] | None = transformation_data.get("filter", None)

        with Image.open(file_path) as img:
            if resize_image:
                pass

            if rotate_image:
                img = img.rotate(rotate_image)




            if filter_image:
                filter_image = transformation_data["filter"]
                grayscale = filter_image.get("graysclae", None)
                sepia = filter_image.get("sepia", None)
                if grayscale:
                    img = img.convert("L")
                if sepia:
                    img = img.convert("RGB")

            img.save(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error on image transformation: {e}",
        )

