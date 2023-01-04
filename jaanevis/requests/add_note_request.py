from jaanevis.domain.note import Note
from jaanevis.requests import InvalidRequestObject, RequestObject, ValidRequestObject


class AddNoteRequest(ValidRequestObject):
    """Request object for adding a new note"""

    def __init__(self, note: Note) -> None:
        self.note = note

    @classmethod
    def build(cls, note: Note) -> RequestObject:

        invalid_req = InvalidRequestObject()

        if not isinstance(note, Note):
            invalid_req.add_error("body", "Invalid note type")
            return invalid_req

        return cls(note=note)
