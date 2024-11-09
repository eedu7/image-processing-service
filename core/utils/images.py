import time
from typing import Tuple, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np


def decode_image(image_bytes: bytes) -> Image:
    """
    Decode an image from bytes.

    Args:
        image_bytes (bytes): The image in bytes.

    Returns:
        Image: The decoded image as a Pillow Image object.
    """
    return Image.open(io.BytesIO(image_bytes))


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
    resized = image.resize((width, height))
    img_byte_arr = io.BytesIO()
    resized.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


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
    cropped = image.crop((x, y, x + width, y + height))
    img_byte_arr = io.BytesIO()
    cropped.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


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
    rotated = image.rotate(angle, expand=True)
    img_byte_arr = io.BytesIO()
    rotated.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


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
        color (Tuple[int, int, int]): The color of the watermark text in RGB format.
        thickness (int): The thickness of the watermark text.

    Returns:
        bytes: The image with the watermark in bytes.
    """
    image = decode_image(image_bytes)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text(position, watermark_text, font=font, fill=color)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


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
        filtered = image.convert("L")
    elif filter_type == "sepia":
        sepia_image = np.array(image)
        sepia_filter = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
        sepia_image = np.dot(sepia_image[...,:3], sepia_filter.T)
        sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
        filtered = Image.fromarray(sepia_image)
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

    img_byte_arr = io.BytesIO()
    filtered.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


def apply_image_transformations(
    image_bytes: bytes,
    transformations: Dict[str, Any],
    original_format: str,
) -> bytes:
    """
    Applies a series of transformations to the image, preserving the original format unless specified.

    Args:
        image_bytes (bytes): The original image in bytes.
        transformations (dict): A dictionary of transformations to apply.
            - resize: {"width": int, "height": int}
            - crop: {"x": int, "y": int, "width": int, "height": int}
            - rotate: int (degrees)
            - watermark: str (text to add as a watermark)
            - filter: {"grayscale": bool, "sepia": bool}
            - format: Optional[str] (desired output format, e.g., "jpg", "png")
        original_format (str): The original format of the image (e.g., "png", "jpeg").

    Returns:
        bytes: The transformed image in bytes.

    Raises:
        ValueError: If the format is unsupported or encoding fails.
    """
    # Apply transformations step by step
    resize = transformations.get("resize", None)
    crop = transformations.get("crop", None)
    rotate = transformations.get("rotate", None)
    watermark = transformations.get("watermark", None)
    filter_image = transformations.get("filter", None)

    if resize is not None:
        image_bytes = resize_image(image_bytes, resize["width"], resize["height"])

    if crop is not None:
        image_bytes = crop_image(image_bytes, crop["x"], crop["y"], crop["width"], crop["height"])

    if rotate is not None:
        image_bytes = rotate_image(image_bytes, transformations["rotate"])

    if watermark is not None:
        image_bytes = add_watermark(image_bytes, transformations["watermark"])

    if filter_image is not None:
        if transformations["filter"].get("grayscale", False):
            image_bytes = apply_filter(image_bytes, "grayscale")
        elif transformations["filter"].get("sepia", False):
            image_bytes = apply_filter(image_bytes, "sepia")

    # Handle format change or preserve original format
    format_image = transformations.get("format", original_format).lower()
    if format_image == "string":
        format_image = original_format
    valid_formats = {"jpg", "jpeg", "png"}
    if format_image not in valid_formats:
        raise ValueError(f"Unsupported format: {format_image}")

    # Convert the image to the desired or original format
    img = decode_image(image_bytes)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format_image.upper())
    return img_byte_arr.getvalue()
