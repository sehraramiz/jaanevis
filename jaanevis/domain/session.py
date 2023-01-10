import uuid
from dataclasses import asdict, field
from typing import Any

from pydantic import UUID4, dataclasses


@dataclasses.dataclass
class Session:
    """Model for session."""

    username: str
    session_id: UUID4 = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["session_id"] = str(self.session_id)
        return data
