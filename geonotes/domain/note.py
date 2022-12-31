import uuid
from dataclasses import asdict, field
from typing import Any

from pydantic import UUID4, BaseModel, dataclasses


@dataclasses.dataclass
class Note:
    """Model for taking note on a location."""

    creator: str
    url: str
    lat: float
    long: float
    code: UUID4 = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["code"] = str(self.code)
        return data


class NoteCreateApi(BaseModel):
    """schema for creating a note via api"""

    url: str
    lat: float
    long: float
