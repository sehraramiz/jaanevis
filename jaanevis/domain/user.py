from dataclasses import asdict
from typing import Any

from pydantic import dataclasses


@dataclasses.dataclass
class User:
    """Model for user."""

    username: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data
