from pydantic import BaseModel, Field


class Resize(BaseModel):
    width: int
    height: int

class Crop(BaseModel):
    width: int
    height: int
    x: int
    y: int

class Filter(BaseModel):
    grayscale: bool
    sepia: bool


class TransformationalModel(BaseModel):
    resize: Resize | None = Field(None, alias='resize', description="Resize")
    crop: Crop | None = Field(None, alias='crop', description="Crop")
    filter: Filter | None = Field(None, alias='filter', description="Filter")
    rotate: int | None = Field(None, alias='rotate', description="Rotate", ge=0, le=360)
    format: str | None = Field(None, alias='format', description="Format")
