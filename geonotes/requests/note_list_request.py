from typing import Any, Mapping, Optional

from geonotes.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class NoteListRequest(ValidRequestObject):
    """Request object for list of notes"""

    accepted_filters = ["code__eq", "url__eq", "lat__eq", "long__eq"]

    def __init__(self, filters: Optional[dict[str, Any]] = None) -> None:
        self.filters = filters

    @classmethod
    def from_dict(cls, data: dict) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if "filters" in data:
            if not isinstance(data["filters"], Mapping):
                invalid_req.add_error("filters", "Is not iterable")
                return invalid_req

            for key, _value in data["filters"].items():
                if key not in cls.accepted_filters:
                    invalid_req.add_error(
                        "filters",
                        f"key {key} cannot be used",
                    )

        if invalid_req.has_errors():
            return invalid_req

        return cls(filters=data.get("filters", None))
