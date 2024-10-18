from pathlib import Path
from typing import Dict, Optional

from PIL import Image

from schema.image import TransformationModel


def transform_image(file_path: Path, transformation_data: TransformationModel) -> Path:
    """
    Applies transformations such as resizing, cropping, rotating, filters, and format changes to the image.

    - **file_path**: Path to the image.
    - **transformation_data**: Transformation details (resize, crop, rotate, filters, format).

    Returns:
    - **Path**: The output file path after transformation.
    """
    with Image.open(file_path) as img:
        data = transformation_data.model_dump()
        resize_image: Dict[str, Optional[float]] = data.get("resize", None)
        crop_image = data.get("crop", None)
        rotate_image: Optional[float] = data.get("rotate", None)
        format_image: Optional[str] = data.get("format", None)
        filter_image: Dict[str, Optional[bool]] = data.get("filter", None)

        if resize_image:
            img = resize_logic(img, resize_image)

        if crop_image:
            img = crop_logic(img, crop_image)

        if rotate_image:
            img = img.rotate(rotate_image)

        if filter_image:
            img = apply_filters(img, filter_image)

        output_format = (
            format_image.lower()
            if format_image != "string"
            else file_path.suffix.lstrip(".")
        )
        output_file_path = file_path.with_suffix(f".{output_format}")
        img.save(output_file_path, output_format.upper())

        return output_file_path


def resize_logic(img, resize_image: Dict[str, Optional[float]]):
    """Handles image resizing."""
    width = resize_image.get("width")
    height = resize_image.get("height")

    if width and height:
        img = img.resize((width, height))
    elif width:
        aspect_ratio = img.height / img.width
        height = int(width * aspect_ratio)
        img = img.resize((width, height))
    elif height:
        aspect_ratio = img.width / img.height
        width = int(height * aspect_ratio)
        img = img.resize((width, height))
    return img


def crop_logic(img, crop_image: Dict[str, int]):
    """Handles image cropping."""
    x = crop_image.get("x", 0)
    y = crop_image.get("y", 0)
    crop_width = crop_image.get("width")
    crop_height = crop_image.get("height")

    if crop_width and crop_height:
        crop_box = (x, y, x + crop_width, y + crop_height)
        img = img.crop(crop_box)
    return img


def apply_filters(img, filter_image: Dict[str, Optional[bool]]):
    """Applies grayscale or sepia filters."""
    grayscale = filter_image.get("grayscale", None)
    sepia = filter_image.get("sepia", None)

    if grayscale:
        img = img.convert("L")
    if sepia:
        img = img.convert("RGB")
        sepia_img = [
            (
                int(0.393 * r + 0.769 * g + 0.189 * b),
                int(0.349 * r + 0.686 * g + 0.168 * b),
                int(0.272 * r + 0.534 * g + 0.131 * b),
            )
            for r, g, b in img.getdata()
        ]
        img.putdata(sepia_img)
    return img
