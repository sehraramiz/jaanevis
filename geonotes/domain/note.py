from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Note:
    """Model for taking note on a location."""

    code: str
    creator: str
    url: str
    lat: float
    long: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
