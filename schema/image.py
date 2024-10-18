from pydantic import BaseModel, Field


class ResizeModel(BaseModel):
    width: int | None = Field(
        None, description="Width of the image in pixels, must be greater than 0", gt=0
    )
    height: int | None = Field(
        None, description="Height of the image in pixels, must be greater than 0", gt=0
    )


class CropModel(BaseModel):
    width: int | None = Field(
        None, description="Width of the cropped area, must be greater than 0", gt=0
    )
    height: int | None = Field(
        None, description="Height of the cropped area, must be greater than 0", gt=0
    )
    x: int | None = Field(
        None,
        description="X-coordinate of the top-left corner for the crop, must be greater than 0",
        gt=0,
    )
    y: int | None = Field(
        None,
        description="Y-coordinate of the top-left corner for the crop, must be greater than 0",
        gt=0,
    )


class FilterModel(BaseModel):
    grayscale: bool = Field(False, description="Apply grayscale filter if set to True")
    sepia: bool = Field(False, description="Apply sepia filter if set to True")


class TransformationModel(BaseModel):
    resize: ResizeModel | None = Field(
        None, description="Resizing transformation options"
    )
    crop: CropModel | None = Field(None, description="Cropping transformation options")
    rotate: int = Field(
        None,
        description="Rotation angle in degrees, must be between 0 and 360",
        ge=0,
        le=360,
    )
    format: str | None = Field(
        None, description="Output image format, must be .jpg, .jpeg, or .png"
    )
    filter: FilterModel | None = Field(
        None, description="Filter options such as grayscale or sepia"
    )

