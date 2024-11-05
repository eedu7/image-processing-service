from typing import Optional

from pydantic import BaseModel, Field


class ResizeImage(BaseModel):
    width: Optional[int] = Field(None)
    height: Optional[int] = Field(None)


class CropImage(BaseModel):
    x: Optional[int] = Field(None)
    y: Optional[int] = Field(None)
    width: Optional[int] = Field(None)
    height: Optional[int] = Field(None)


class FilterImage(BaseModel):
    grayscale: Optional[bool] = Field(None)
    sepia: Optional[bool] = Field(None)


class ImageTransformation(BaseModel):
    resize: Optional[ResizeImage] = Field(None)
    crop: Optional[CropImage] = Field(None)
    rotate: Optional[int] = Field(None)
    format: Optional[str] = Field(None)
    watermark: Optional[str] = Field(None)
    filter: Optional[FilterImage] = Field(None)
