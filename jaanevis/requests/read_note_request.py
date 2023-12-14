from jaanevis.i18n import gettext as _
from jaanevis.requests import (
    InvalidRequestObject,
    RequestObject,
    ValidRequestObject,
)


class ReadNoteRequest(ValidRequestObject):
    """request to read a note by it's code"""

    def __init__(self, code: str) -> None:
        self.code = code

    @classmethod
    def build(cls, code: str) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not code:
            invalid_req.add_error("code", _("Invalid code value"))
            return invalid_req

        return cls(code=code)
