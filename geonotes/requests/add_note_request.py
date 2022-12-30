from geonotes.domain.note import Note
from geonotes.requests import InvalidRequestObject, RequestObject


class AddNoteRequest:
    def __new__(self, note: Note) -> RequestObject:
        invalid_req = InvalidRequestObject()

        if not isinstance(note, Note):
            invalid_req.add_error("body", "Invalid note type")
            return invalid_req

        self.note = note
        return self
