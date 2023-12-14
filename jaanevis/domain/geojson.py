"""models for GeoJson objects"""

from typing import Any, Tuple

from pydantic import BaseModel, Field


class GeoJsonPoint(BaseModel):
    type: str = Field(init=False, default="Point")
    coordinates: Tuple[float, float] = Field(description="[long, lat]")


class GeoJsonFeature(BaseModel):
    type: str = Field(init=False, default="Feature")
    geometry: GeoJsonPoint
    properties: Any
