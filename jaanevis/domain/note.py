import re
import uuid
from dataclasses import asdict, field
from datetime import datetime
from typing import Any, Optional

from pydantic import UUID4, AnyHttpUrl, BaseModel, dataclasses, validator
from pytz import timezone

from jaanevis.config import settings
from jaanevis.domain.geojson import GeoJsonFeature
from jaanevis.utils import geo


def datetime_with_tz():
    TZ = timezone(settings.TZ)
    return datetime.now(TZ)


@dataclasses.dataclass
class Note:
    """Model for taking note on a location."""

    url: AnyHttpUrl
    lat: float
    long: float
    country: str = ""
    text: str = ""
    tags: list[str] = field(default_factory=list)
    code: str | UUID4 = field(default_factory=uuid.uuid4)
    creator_id: Optional[str] = None
    creator: Optional[str] = None
    created: datetime = field(default_factory=datetime_with_tz)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["code"] = str(self.code)
        data["url"] = str(self.url)
        data["created"] = self.created.isoformat()
        return data

    def __post_init__(self):
        if not self.country:
            self.country = geo.get_country_from_latlong(self.lat, self.long)
        if not self.tags and "#" in self.text:
            r = "#(\\w+)"
            self.tags = re.findall(r, self.text)


class NoteRead(BaseModel):
    """schema for reading note without private fields"""

    url: str | None = None
    lat: float | None = None
    long: float | None = None
    country: str | None = ""
    text: str | None = ""
    tags: list[str] | None = None
    code: str | None = None
    creator: str | None = None
    created: datetime | None = None

    @validator("created")
    def created_str(cls, value):
        return value.isoformat()


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
    code: str | UUID4
    text: str = ""


class NoteGeoJsonFeature(GeoJsonFeature):
    properties: NoteGeoJsonProperties
