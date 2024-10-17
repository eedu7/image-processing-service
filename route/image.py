import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

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
