from jaanevis.domain.note import NoteUpdateApi
from jaanevis.domain.user import User
from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class UpdateNoteRequest(ValidRequestObject):
    """request object to update a note"""

    def __init__(self, code: str, note: NoteUpdateApi, user: User) -> None:
        self.note = note
        self.code = code
        self.user = user

    @classmethod
    def build(
        cls, code: str, note: NoteUpdateApi, user: User
    ) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not isinstance(note, NoteUpdateApi):
            invalid_req.add_error("body", "Invalid note type")
            return invalid_req
        if not code:
            invalid_req.add_error("code", "Invalid code")
            return invalid_req
        if not user:
            invalid_req.add_error("user", "Invalid user")
            return invalid_req
        return cls(code=code, note=note, user=user)
