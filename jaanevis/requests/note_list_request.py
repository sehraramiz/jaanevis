from typing import Any, Mapping, Optional

from jaanevis.i18n import gettext as _
from jaanevis.requests import (
    InvalidRequestObject,
    RequestObject,
    ValidRequestObject,
)


class NoteListRequest(ValidRequestObject):
    """Request object for list of notes"""

    accepted_filters = [
        "code__eq",
        "url__eq",
        "lat__eq",
        "long__eq",
        "creator__eq",
        "country__eq",
        "tag__eq",
    ]

    def __init__(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: int = None,
        skip: int = 0,
    ) -> None:
        self.filters = filters
        self.limit = limit
        self.skip = skip

    @classmethod
    def from_dict(cls, data: dict) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if "filters" in data:
            if not isinstance(data["filters"], Mapping):
                invalid_req.add_error("filters", _("Invalid filters type"))
                return invalid_req

            filters_copy = data["filters"].copy()
            for key, _value in filters_copy.items():
                if key not in cls.accepted_filters:
                    invalid_req.add_error(
                        "filters",
                        f"key {key} cannot be used",
                    )
                if _value is None:
                    data["filters"].pop(key)

        if invalid_req.has_errors():
            return invalid_req

        return cls(
            filters=data.get("filters", None),
            limit=data.get("limit"),
            skip=data.get("skip", 0),
        )
