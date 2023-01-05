from jaanevis.domain.note import NoteUpdateApi
from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class UpdateNoteRequest(ValidRequestObject):
    """request object to update a note"""

    def __init__(self, code: str, note: NoteUpdateApi) -> None:
        self.note = note
        self.code = code

    @classmethod
    def build(cls, code: str, note: NoteUpdateApi) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not isinstance(note, NoteUpdateApi):
            invalid_req.add_error("body", "Invalid note type")
            return invalid_req

        if not code:
            invalid_req.add_error("code", "Invalid code")
            return invalid_req

        return cls(code=code, note=note)
