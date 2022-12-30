import uuid
from dataclasses import asdict, field
from typing import Any

from pydantic import UUID4, dataclasses


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
        self.code = str(self.code)
        return asdict(self)
