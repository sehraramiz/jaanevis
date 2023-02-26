from dataclasses import asdict
from typing import Any

from pydantic import BaseModel, dataclasses


@dataclasses.dataclass
class User:
    """Model for user."""

    email: str
    username: str
    password: str
    is_active: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data


class UserRead(BaseModel):
    """schema for user without password"""

    username: str
    is_active: bool = False


class UserUpdateApi(BaseModel):
    """schema for updatig a user via api"""

    username: str | None = None
