from typing import Optional, Protocol

from jaanevis.domain import note as n
from jaanevis.domain import session as s
from jaanevis.domain import user as u
from jaanevis.repository import memrepo as mr


class Repository(Protocol):
    """base data repository protocol"""

    def list(
        self, filters: Optional[dict] = None, limit: int = None, skip: int = 0
    ) -> list[n.Note]:
        ...

    def add(self, note: n.Note) -> None:
        ...

    def get_by_code(self, code: str) -> n.Note:
        ...

    def delete_by_code(self, code: str) -> n.Note:
        ...

    def update(self, obj: n.Note, data: dict) -> n.Note:
        ...

    def get_user_by_username(self, username: str) -> u.User:
        ...

    def get_user_by_email(self, email: str) -> u.User:
        ...

    def create_user(self, username: str, password: str) -> u.User:
        ...

    def update_user(self, obj: u.User, data: str) -> u.User:
        ...

    def delete_user(self, username: str) -> bool:
        ...

    def get_session_by_session_id(self, session_id: str) -> s.Session:
        ...

    def get_session_by_session_id_and_email(
        self, session_id: str, email: str
    ) -> s.Session:
        ...

    def get_session_by_session_id_and_username(
        self, session_id: str, username: str
    ) -> s.Session:
        ...

    def delete_session_by_session_id(self, session_id: str) -> bool:
        ...

    def create_session(
        self, username: str, session_id: str, expire_time: float
    ) -> s.Session:
        ...

    def create_or_update_session(
        self, username: str, session_id: str, expire_time: float
    ) -> s.Session:
        ...


repository: Repository = mr.MemRepo
