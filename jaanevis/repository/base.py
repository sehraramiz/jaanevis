from typing import Optional, Protocol

from jaanevis.domain import note as n


class Repository(Protocol):
    """base data repository protocol"""

    def list(self, filters: Optional[dict] = None) -> list[n.Note]:
        ...

    def add(self, note: n.Note) -> None:
        ...

    def get_by_code(self, code: str) -> n.Note:
        ...
