import os
import time
from typing import Any, Tuple

import cv2
import numpy as np
from fastapi import UploadFile

from core.exceptions import BadRequestException, NotFoundException


def create_file_name(file_name: str) -> str:
    file_name: str = str(int(time.time())) + file_name.replace(" ", "")
    return file_name


def read_image(file_name: str) -> Any:
    file_path = f"images/{file_name}"
    if not os.path.exists(file_path):
        raise NotFoundException("File does not exist")

    image = cv2.imread(file_path)
    if image is None:
        raise BadRequestException(f"Failed to read image: {file_path}")

    return image


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


def remove_image(file_name: str) -> None:
    file_path = f"images/{file_name}"

    if not os.path.exists(file_path):
        raise BadRequestException(f"Image file does not exist: {file_path}")

    try:
        os.remove(file_path)
    except Exception as e:
        raise BadRequestException(f"Failed to delete image: {e}")


def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    return cv2.resize(image, (width, height))


def crop_image(
    image: np.ndarray, x: int, y: int, width: int, height: int
) -> np.ndarray:
    return image[y : y + height, x : x + width]


def rotate_image(image: np.ndarray, angle: int) -> np.ndarray:
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))


def add_watermark(
    image: np.ndarray,
    watermark_text: str,
    position: Tuple[int, int] = (10, 10),
    font_scale: float = 1.0,
    color: Tuple[int, int, int] = (255, 255, 255),
    thickness: int = 2,
) -> np.ndarray:
    return cv2.putText(
        image.copy(),
        watermark_text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
    )


def flip_image(image: np.ndarray, flip_code: int) -> np.ndarray:
    return cv2.flip(image, flip_code)


def mirror_image(image: np.ndarray) -> np.ndarray:
    return flip_image(image, flip_code=1)


def compress_image(image: np.ndarray, quality: int = 90) -> np.ndarray:
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encoded_img = cv2.imencode(".jpg", image, encode_param)
    if not result:
        raise BadRequestException("Failed to compress image")
    return cv2.imdecode(encoded_img, 1)


def change_format(image: np.ndarray, new_format: str) -> bytes:
    encoded_param = (
        [int(cv2.IMWRITE_JPEG_QUALITY), 90] if new_format.lower() == "jpg" else []
    )
    result, encoded_img = cv2.imencode(f".{new_format}", image, encoded_param)
    if not result:
        raise BadRequestException("Failed to change image format")
    return encoded_img.tobytes()


def apply_filter(image: np.ndarray, filter_type: str) -> np.ndarray:
    if filter_type == "grayscale":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == "sepia":
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        sepia_image = cv2.transform(image, kernel)
        return np.clip(sepia_image, 0, 255).astype(np.uint8)
    else:
        raise BadRequestException(f"Unknown filter type: {filter_type}")


def save_image(image: np.ndarray, file_name: str, folder: str = "images") -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, file_name)
    cv2.imwrite(file_path, image)
    return file_path


def process_image(file_name: str):
    # Load the image (simulating fetching it once)
    image = read_image(file_name)

    # Apply transformations
    image = resize_image(image, width=300, height=300)
    image = crop_image(image, x=10, y=10, width=200, height=200)
    image = rotate_image(image, angle=45)
    image = add_watermark(image, watermark_text="Sample Watermark")
    image = mirror_image(image)
    image = compress_image(image, quality=80)
    image = apply_filter(image, filter_type="sepia")

    # Save final image
    final_file_path = save_image(image, file_name)
    print(f"Transformed image saved at: {final_file_path}")
