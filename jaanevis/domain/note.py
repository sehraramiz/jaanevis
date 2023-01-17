import re
import uuid
from dataclasses import asdict, field
from typing import Any, Optional

from pydantic import UUID4, AnyHttpUrl, BaseModel, dataclasses

from jaanevis.domain.geojson import GeoJsonFeature
from jaanevis.utils import geo


@dataclasses.dataclass
class Note:
    """Model for taking note on a location."""

    url: AnyHttpUrl
    lat: float
    long: float
    country: str = ""
    text: str = ""
    tags: list[str] = field(default_factory=list)
    code: UUID4 = field(default_factory=uuid.uuid4)
    creator: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["code"] = str(self.code)
        data["url"] = str(self.url)
        return data

    def __post_init__(self):
        if not self.country:
            self.country = geo.get_country_from_latlong(self.lat, self.long)
        if not self.tags and "#" in self.text:
            r = "#(\\w+)"
            self.tags = re.findall(r, self.text)


class NoteCreateApi(BaseModel):
    """schema for creating a note via api"""

    url: AnyHttpUrl
    text: str = ""
    lat: float
    long: float


class NoteUpdateApi(BaseModel):
    """schema for updatig a note via api"""

    url: Optional[AnyHttpUrl] = None
    text: Optional[str] = ""
    lat: Optional[float] = None
    long: Optional[float] = None


class NoteGeoJsonProperties(BaseModel):
    url: AnyHttpUrl
    creator: str
    country: str
    code: UUID4
    text: str = ""


class NoteGeoJsonFeature(GeoJsonFeature):
    properties: NoteGeoJsonProperties
