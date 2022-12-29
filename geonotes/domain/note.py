import uuid
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Note:
    """Model for taking note on a location."""

    creator: str
    url: str
    lat: float
    long: float
    code: str = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
