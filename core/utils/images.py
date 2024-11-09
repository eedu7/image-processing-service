import time
from typing import Tuple

import cv2
import numpy as np

from core.exceptions import BadRequestException


def decode_image(image_bytes: bytes) -> np.ndarray:
    """
    Decode an image from bytes.

    Args:
        image_bytes (bytes): The image in bytes.

    Returns:
        np.ndarray: The decoded image as a NumPy array.
    """
    return cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)


def create_file_name(file_name: str) -> str:
    """
    Create a unique file name by appending the current timestamp to the given file name.

    Args:
        file_name (str): The original file name.

    Returns:
        str: The new file name with a timestamp prefix.
    """
    return str(int(time.time())) + file_name.replace(" ", "")


def resize_image(image_bytes: bytes, width: int, height: int) -> bytes:
    """
    Resize an image to the specified dimensions.

    Args:
        image_bytes (bytes): The image in bytes.
        width (int): The desired width of the image.
        height (int): The desired height of the image.

    Returns:
        bytes: The resized image in bytes.
    """
    image = decode_image(image_bytes)
    resized = cv2.resize(image, (width, height))
    _, output_bytes = cv2.imencode(".jpg", resized)
    return output_bytes.tobytes()


def crop_image(image_bytes: bytes, x: int, y: int, width: int, height: int) -> bytes:
    """
    Crop an image to the specified rectangle.

    Args:
        image_bytes (bytes): The image in bytes.
        x (int): The x-coordinate of the top-left corner of the crop area.
        y (int): The y-coordinate of the top-left corner of the crop area.
        width (int): The width of the crop area.
        height (int): The height of the crop area.

    Returns:
        bytes: The cropped image in bytes.
    """
    image = decode_image(image_bytes)
    cropped = image[y : y + height, x : x + width]
    _, output_bytes = cv2.imencode(".jpg", cropped)
    return output_bytes.tobytes()


def rotate_image(image_bytes: bytes, angle: int) -> bytes:
    """
    Rotate an image by the specified angle around its center.

    Args:
        image_bytes (bytes): The image in bytes.
        angle (int): The angle in degrees to rotate the image.

    Returns:
        bytes: The rotated image in bytes.
    """
    image = decode_image(image_bytes)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h))
    _, output_bytes = cv2.imencode(".jpg", rotated)
    return output_bytes.tobytes()


def add_watermark(
    image_bytes: bytes,
    watermark_text: str,
    position: Tuple[int, int] = (10, 10),
    font_scale: float = 1.0,
    color: Tuple[int, int, int] = (255, 255, 255),
    thickness: int = 2,
) -> bytes:
    """
    Add a text watermark to an image.

    Args:
        image_bytes (bytes): The image in bytes.
        watermark_text (str): The text to use as the watermark.
        position (Tuple[int, int]): The position of the watermark text.
        font_scale (float): The font scale of the watermark text.
        color (Tuple[int, int, int]): The color of the watermark text in BGR format.
        thickness (int): The thickness of the watermark text.

    Returns:
        bytes: The image with the watermark in bytes.
    """
    image = decode_image(image_bytes)
    watermarked = cv2.putText(
        image.copy(),
        watermark_text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
    )
    _, output_bytes = cv2.imencode(".jpg", watermarked)
    return output_bytes.tobytes()


def apply_filter(image_bytes: bytes, filter_type: str) -> bytes:
    """
    Apply a specified filter to an image.

    Args:
        image_bytes (bytes): The image in bytes.
        filter_type (str): The type of filter to apply ("grayscale" or "sepia").

    Returns:
        bytes: The filtered image in bytes.
    """
    image = decode_image(image_bytes)
    if filter_type == "grayscale":
        filtered = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == "sepia":
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        sepia_image = cv2.transform(image, kernel)
        filtered = np.clip(sepia_image, 0, 255).astype(np.uint8)
    else:
        raise BadRequestException(f"Unknown filter type: {filter_type}")

    _, output_bytes = cv2.imencode(".jpg", filtered)
    return output_bytes.tobytes()
