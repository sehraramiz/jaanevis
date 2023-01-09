import logging
import sys
from typing import Optional

sys.path = ["", ".."] + sys.path[1:]

from jaanevis.domain.note import Note, NoteCreateApi
from jaanevis.repository import repository
from jaanevis.requests.add_note_request import AddNoteRequest
from jaanevis.requests.note_list_request import NoteListRequest
from jaanevis.responses import ResponseObject
from jaanevis.usecases.add_note import AddNoteUseCase
from jaanevis.usecases.note_list import NoteListUseCase

logger = logging.getLogger(__name__)


def get_notes_list(filters: Optional[dict]) -> ResponseObject:
    qrystr_params = {"filters": filters or {}}

    request_obj = NoteListRequest.from_dict(qrystr_params)

    repo = repository()
    usecase = NoteListUseCase(repo)
    response = usecase.execute(request_obj)
    return response


def add_note(note_in: NoteCreateApi) -> ResponseObject:
    note = Note(**note_in.dict(), creator="default")
    request_obj = AddNoteRequest.build(note)

    repo = repository()
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
