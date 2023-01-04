import logging
import sys
import uuid
from typing import Optional

sys.path = ["", ".."] + sys.path[1:]

from jaanevis.domain.note import Note, NoteCreateApi
from jaanevis.repository import memrepo as mr
from jaanevis.requests.add_note_request import AddNoteRequest
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.responses import ResponseObject
from jaanevis.usecases.add_note import AddNoteUseCase
from jaanevis.usecases.note_list import NoteListUseCase

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


def get_notes_list(filters: Optional[dict]) -> ResponseObject:
    qrystr_params = {"filters": filters or {}}

    request_obj = NoteListRequest.from_dict(qrystr_params)

    repo = mr.MemRepo(note_dicts)
    usecase = NoteListUseCase(repo)
    response = usecase.execute(request_obj)
    return response


def add_note(note_in: NoteCreateApi) -> ResponseObject:
    note = Note(**note_in.dict(), creator="default")
    request_obj = AddNoteRequest(note)

    repo = mr.MemRepo(note_dicts)
    usecase = AddNoteUseCase(repo)
    response = usecase.execute(request_obj)
    return response


if __name__ == "__main__":
    notes = get_notes_list(filters={})
    print(notes.value)

    new_note = NoteCreateApi(
        url="https://example.com/1",
        lat=1,
        long=1,
    )
    note_add_res = add_note(new_note)
    print(note_add_res.value)
