from jaanevis.domain.note import Note
from jaanevis.domain.user import User
from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class AddNoteRequest(ValidRequestObject):
    """Request object for adding a new note"""

    def __init__(self, note: Note, user: User) -> None:
        self.note = note
        self.user = user

    @classmethod
    def build(cls, note: Note, user: User) -> RequestObject:

        invalid_req = InvalidRequestObject()

        if not isinstance(note, Note):
            invalid_req.add_error("body", "Invalid note type")
            return invalid_req

        if not user or not isinstance(user, User):
            invalid_req.add_error("user", "Invalid user")
            return invalid_req

        return cls(note=note, user=user)
