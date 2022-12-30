import logging
import sys
import uuid

sys.path = ["", ".."] + sys.path[1:]

from geonotes.domain.note import Note
from geonotes.repository import memrepo as mr
from geonotes.requests.add_note_request import AddNoteRequest
from geonotes.requests.note_list_request import NoteListRequest
from geonotes.responses import ResponseObject
from geonotes.usecases.add_note import AddNoteUseCase
from geonotes.usecases.note_list import NoteListUseCase

logger = logging.getLogger(__name__)

note_1 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/1",
    "lat": 1,
    "long": 1,
}

note_2 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/2",
    "lat": 2,
    "long": 2,
}

note_3 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/3",
    "lat": 1,
    "long": 1,
}

note_4 = {
    "code": uuid.uuid4(),
    "creator": "default",
    "url": "https://example.com/4",
    "lat": 4,
    "long": 4,
}

note_dicts = [note_1, note_2, note_3, note_4]


def get_notes_list(filters: dict = None) -> ResponseObject:
    qrystr_params = {"filters": filters or {}}

    request_obj = NoteListRequest.from_dict(qrystr_params)

    repo = mr.MemRepo(note_dicts)
    usecase = NoteListUseCase(repo)
    response = usecase.execute(request_obj)
    return response


def add_note(note: Note) -> ResponseObject:
    request_obj = AddNoteRequest(note)

    repo = mr.MemRepo(note_dicts)
    usecase = AddNoteUseCase(repo)
    response = usecase.execute(request_obj)
    return response


if __name__ == "__main__":
    notes = get_notes_list()
    print(notes.value)
    new_note = Note(
        creator="default",
        url="https://example.com/1",
        lat=1,
        long=1,
    )
    note_add_res = add_note(new_note)
    print(note_add_res.value)
