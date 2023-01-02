import uuid
from dataclasses import asdict, field
from typing import Any

from pydantic import UUID4, AnyHttpUrl, BaseModel, dataclasses

from geonotes.domain.geojson import GeoJsonFeature


@dataclasses.dataclass
class Note:
    """Model for taking note on a location."""

    creator: str
    url: AnyHttpUrl
    lat: float
    long: float
    code: UUID4 = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["code"] = str(self.code)
        data["url"] = str(self.url)
        return data


class NoteCreateApi(BaseModel):
    """schema for creating a note via api"""

    url: AnyHttpUrl
    lat: float
    long: float


class NoteGeoJsonProperties(BaseModel):
    url: AnyHttpUrl
    creator: str
    code: UUID4


class NoteGeoJsonFeature(GeoJsonFeature):
    properties: NoteGeoJsonProperties
