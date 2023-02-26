import uuid
from dataclasses import asdict, field
from datetime import datetime, timedelta
from typing import Any

from pydantic import UUID4, BaseModel, EmailStr, dataclasses


def default_expire_time() -> float:
    return (datetime.now() + timedelta(days=1)).timestamp()


@dataclasses.dataclass
class Session:
    """Model for session."""

    username: str
    expire_time: float = field(default_factory=default_expire_time)
    session_id: str | UUID4 = field(default_factory=uuid.uuid4)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["session_id"] = str(self.session_id)
        return data


class LoginInputApi(BaseModel):
    """schema for user login via api"""

    username: str
    password: str


class RegisterInputApi(BaseModel):
    """schema for user registeration via api"""

    email: EmailStr
    username: str
    password: str
