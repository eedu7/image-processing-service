import os
import time
from typing import Tuple
from fastapi import UploadFile

from core.exceptions import BadRequestException


def create_file_name(file_name: str) -> str:
    file_name: str = str(int(time.time())) + file_name.replace(" ", "")
    return file_name


def save_uploaded_image(image: UploadFile, folder: str = "images") -> Tuple[str, str]:
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_name: str = create_file_name(image.filename)

    file_path = os.path.join(folder, file_name)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())
    except Exception as e:
        raise BadRequestException(f"Failed to save image: {e}")

    return file_path, file_name
