from jaanevis.domain import user as u
from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class DeleteNoteRequest(ValidRequestObject):
    """request to delete a note by it's code"""

    def __init__(self, code: str, user: u.User) -> None:
        self.code = code
        self.user = user

    @classmethod
    def build(cls, code: str, user: u.User) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not code:
            invalid_req.add_error("code", _("Invalid code value"))
            return invalid_req

        if not user:
            invalid_req.add_error("user", _("Invalid user"))
            return invalid_req

        return cls(code=code, user=user)
